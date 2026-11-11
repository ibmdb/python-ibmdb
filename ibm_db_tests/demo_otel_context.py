"""Demonstrate automatic W3C context propagation through ibm_db."""

import os
import secrets
import sys

import ibm_db
import ibm_db_dbi
from opentelemetry import baggage, context, trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.trace import (
    NonRecordingSpan,
    SpanContext,
    TraceFlags,
    TraceState,
    set_span_in_context,
)
from opentelemetry.trace.propagation.tracecontext import (
    TraceContextTextMapPropagator,
)


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


FIXED_W3C_HEADERS = {
    "traceparent": "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01",
    "tracestate": "congo=t61rcWkgMzE",
    "baggage": "userId=alice,serverNode=DF28",
}

CHANGED_W3C_HEADERS = {
    "traceparent": "00-fedcba9876543210fedcba9876543210-fedcba9876543210-00",
    "tracestate": "congo=changed",
    "baggage": "userId=bob,serverNode=DF29",
}

OTEL_ATTRIBUTES = (
   ("traceparent", ibm_db.SQL_ATTR_OTEL_TRACEPARENT),
   ("tracestate", ibm_db.SQL_ATTR_OTEL_TRACESTATE),
   ("baggage", ibm_db.SQL_ATTR_OTEL_BAGGAGE),
)


def get_connection_args():
    db2_connstr = os.environ.get("DB2_CONNSTR")
    if db2_connstr:
        return db2_connstr, "", ""

    import config

    return config.database, config.user, config.password


def make_parent_context():
    parent_span = SpanContext(
        trace_id=secrets.randbits(128) or 1,
        span_id=secrets.randbits(64) or 1,
        is_remote=True,
        trace_flags=TraceFlags(TraceFlags.SAMPLED),
        trace_state=TraceState([("demo", "ibm_db")]),
    )
    parent_context = set_span_in_context(NonRecordingSpan(parent_span))
    return baggage.set_baggage(
        "demo", "ibm_db_otel", context=parent_context
    )


def current_w3c_headers():
    headers = {}
    TraceContextTextMapPropagator().inject(headers)
    W3CBaggagePropagator().inject(headers)
    return headers


def show_connection_attributes(conn, expected_headers, dbi=False):
    print("  ibm_db connection attributes:")
    for header, attribute in OTEL_ATTRIBUTES:
        value = (
            conn.get_option(attribute)
            if dbi
            else ibm_db.get_option(conn, attribute, 1)
        )
        if value is False:
            print(f"    {header}: unavailable from this CLI driver")
        else:
            print(f"    {header}: {value}")
            if expected_headers is not None and value != expected_headers.get(
                header, ""
            ):
                raise AssertionError(
                    f"{header} did not match the expected W3C context"
                )


def run_native_query(conn, label, sql, expected_headers):
    stmt = ibm_db.exec_immediate(conn, sql)
    if not stmt:
        raise RuntimeError(f"Failed to execute query: {label}")
    try:
        row = ibm_db.fetch_tuple(stmt)
        print(f"\n{label}: {row[0] if row else '<no row>'}")
    finally:
        ibm_db.free_result(stmt)
    show_connection_attributes(conn, expected_headers)


def run_prepared_query(conn, label, sql, parameters, expected_headers):
    stmt = ibm_db.prepare(conn, sql)
    if not stmt:
        raise RuntimeError(f"Failed to prepare query: {label}")
    try:
        if not ibm_db.execute(stmt, parameters):
            raise RuntimeError(f"Failed to execute prepared query: {label}")
        row = ibm_db.fetch_tuple(stmt)
        print(f"\n{label}: {row[0] if row else '<no row>'}")
    finally:
        ibm_db.free_result(stmt)
    show_connection_attributes(conn, expected_headers)


def run_carrier_case(conn, case_number, headers):
    extracted_context = TraceContextTextMapPropagator().extract(headers)
    extracted_context = W3CBaggagePropagator().extract(
        headers, extracted_context
    )
    token = context.attach(extracted_context)
    try:
        description = (
            "fixed carrier"
            if case_number == 4
            else "changed fixed carrier on the same connection"
        )
        print(
            f"\nCase {case_number}: W3C context extracted from "
            f"the {description}:"
        )
        for header, _attribute in OTEL_ATTRIBUTES:
            print(f"  {header}: {headers[header]}")
        run_native_query(
            conn,
            f"case {case_number} query; current schema",
            "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1",
            headers,
        )
    finally:
        context.detach(token)


def main():
    connection_args = get_connection_args()
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)
    parent_context_token = context.attach(make_parent_context())
    conn = None
    preexisting_conn = None
    dbi_conn = None
    cursor = None
    try:
        with tracer.start_as_current_span("ibm_db.otel_demo"):
            active_headers = current_w3c_headers()
            print(
                "\nCase 1: automatically propagate the active span when "
                "connecting:"
            )
            for header, _attribute in OTEL_ATTRIBUTES:
                print(f"  {header}: {active_headers.get(header, '')}")

            conn = ibm_db.connect(*connection_args)
            print("  attributes immediately after connect, before SQL:")
            show_connection_attributes(conn, active_headers)

            print("\nCase 2: propagate context before ibm_db.exec_immediate:")
            run_native_query(
                conn,
                "current schema",
                "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1",
                active_headers,
            )

            print("\nCase 3: propagate context before prepared ibm_db.execute:")
            run_prepared_query(
                conn,
                "prepared parameter",
                "SELECT CAST(? AS VARCHAR(32)) FROM SYSIBM.SYSDUMMY1",
                ("prepared execution",),
                active_headers,
            )

        for case_number, headers in (
            (4, FIXED_W3C_HEADERS),
            (5, CHANGED_W3C_HEADERS),
        ):
            run_carrier_case(conn, case_number, headers)

        print("\nCase 6: automatically propagate through ibm_db_dbi:")
        with tracer.start_as_current_span("ibm_db_dbi.otel_demo"):
            dbi_headers = current_w3c_headers()
            dbi_conn = ibm_db_dbi.connect(*connection_args)
            cursor = dbi_conn.cursor()
            cursor.execute("SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1")
            row = cursor.fetchone()
            print(f"  current schema: {row[0] if row else '<no row>'}")
            show_connection_attributes(dbi_conn, dbi_headers, dbi=True)

        print(
            "\nCase 7: update context on a connection opened before the span:"
        )
        empty_token = context.attach(context.Context())
        try:
            preexisting_conn = ibm_db.connect(*connection_args)
        finally:
            context.detach(empty_token)
        with tracer.start_as_current_span("ibm_db.otel_existing_connection"):
            existing_headers = current_w3c_headers()
            run_native_query(
                preexisting_conn,
                "query on preexisting connection",
                "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1",
                existing_headers,
            )

        print("\nCase 8: clear automatically propagated values without a span:")
        empty_token = context.attach(context.Context())
        try:
            run_native_query(
                conn,
                "query without active context",
                "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1",
                {"traceparent": "", "tracestate": "", "baggage": ""},
            )
        finally:
            context.detach(empty_token)

        print("\nCase 9: explicit connection attributes take precedence:")
        explicit_headers = {
            "traceparent": (
                "00-11111111111111111111111111111111-2222222222222222-01"
            ),
            "tracestate": "demo=manual",
            "baggage": "demo=manual",
        }
        explicit_attributes = {
            attribute: explicit_headers[header]
            for header, attribute in OTEL_ATTRIBUTES
        }
        with tracer.start_as_current_span("ibm_db.otel_explicit"):
            try:
                result = ibm_db.set_option(conn, explicit_attributes, 1)
            except Exception as error:
                if "does not support OpenTelemetry connection attributes" not in str(
                    error
                ):
                    raise
                print(
                    "  Explicit attributes are unsupported by this CLI driver; "
                    "automatic propagation remains optional."
                )
            else:
                if not result:
                    raise RuntimeError(
                        "ibm_db.set_option failed to set explicit OTEL attributes"
                    )
                run_native_query(
                    conn,
                    "query with explicit attributes",
                    "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1",
                    explicit_headers,
                )
    finally:
        try:
            if cursor is not None:
                cursor.close()
            if dbi_conn is not None:
                dbi_conn.close()
            if preexisting_conn:
                ibm_db.close(preexisting_conn)
            if conn:
                ibm_db.close(conn)
        finally:
            context.detach(parent_context_token)


if __name__ == "__main__":
    main()
