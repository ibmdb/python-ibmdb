import os
import unittest
from unittest.mock import patch

import ibm_db
import ibm_db_dbi


TRACEPARENT = "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01"
TRACESTATE = "congo=t61rcWkgMzE"
BAGGAGE = "userId=alice,serverNode=DF28"
UPDATED_TRACEPARENT = "00-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-bbbbbbbbbbbbbbbb-01"
UPDATED_TRACESTATE = "rojo=00f067aa0ba902b7"
UPDATED_BAGGAGE = "userId=bob,serverNode=DF29"
OTEL_ATTRS = {
    ibm_db.SQL_ATTR_OTEL_TRACEPARENT: TRACEPARENT,
    ibm_db.SQL_ATTR_OTEL_TRACESTATE: TRACESTATE,
    ibm_db.SQL_ATTR_OTEL_BAGGAGE: BAGGAGE,
}
UPDATED_OTEL_ATTRS = {
    ibm_db.SQL_ATTR_OTEL_TRACEPARENT: UPDATED_TRACEPARENT,
    ibm_db.SQL_ATTR_OTEL_TRACESTATE: UPDATED_TRACESTATE,
    ibm_db.SQL_ATTR_OTEL_BAGGAGE: UPDATED_BAGGAGE,
}


class IbmDbTestCase(unittest.TestCase):

    def test_331_OtelContextHelper(self):
        try:
            from opentelemetry import context
            from opentelemetry.baggage.propagation import W3CBaggagePropagator
            from opentelemetry.trace.propagation.tracecontext import (
                TraceContextTextMapPropagator,
            )
        except ImportError:
            self.skipTest("OpenTelemetry API packages are not installed")

        from ibm_db_otel import apply_otel_context

        headers = {
            "traceparent": TRACEPARENT,
            "tracestate": TRACESTATE,
            "baggage": BAGGAGE,
        }
        active = TraceContextTextMapPropagator().extract(headers)
        active = W3CBaggagePropagator().extract(headers, active)
        token = context.attach(active)
        try:
            with patch.object(ibm_db, "set_option", return_value=True) as setter:
                mask = apply_otel_context(object())
            self.assertEqual(mask, 7)
            self.assertEqual(setter.call_args.args[1], OTEL_ATTRS)

            with patch.object(ibm_db, "set_option", return_value=True) as setter:
                mask = apply_otel_context(
                    object(),
                    explicit_attrs=(ibm_db.SQL_ATTR_OTEL_TRACEPARENT,),
                )
            self.assertEqual(mask, 6)
            self.assertEqual(
                setter.call_args.args[1],
                {
                    ibm_db.SQL_ATTR_OTEL_TRACESTATE: TRACESTATE,
                    ibm_db.SQL_ATTR_OTEL_BAGGAGE: BAGGAGE,
                },
            )
        finally:
            context.detach(token)

        token = context.attach(context.Context())
        try:
            with patch.object(ibm_db, "set_option", return_value=True) as setter:
                mask = apply_otel_context(
                    object(),
                    explicit_attrs=(ibm_db.SQL_ATTR_OTEL_TRACEPARENT,),
                    clear_attrs=tuple(OTEL_ATTRS),
                )
            self.assertEqual(mask, 0)
            self.assertEqual(
                setter.call_args.args[1],
                {
                    ibm_db.SQL_ATTR_OTEL_TRACESTATE: "",
                    ibm_db.SQL_ATTR_OTEL_BAGGAGE: "",
                },
            )
        finally:
            context.detach(token)

    def test_331_OtelConnectionAttrs(self):
        self.assertEqual(ibm_db.SQL_ATTR_OTEL_TRACEPARENT, 3056)
        self.assertEqual(ibm_db.SQL_ATTR_OTEL_TRACESTATE, 3057)
        self.assertEqual(ibm_db.SQL_ATTR_OTEL_BAGGAGE, 3058)
        self.assertEqual(ibm_db_dbi.SQL_ATTR_OTEL_TRACEPARENT, 3056)
        self.assertEqual(ibm_db_dbi.SQL_ATTR_OTEL_TRACESTATE, 3057)
        self.assertEqual(ibm_db_dbi.SQL_ATTR_OTEL_BAGGAGE, 3058)
        self._test_manual_and_automatic_context()

    def _test_manual_and_automatic_context(self):
        try:
            from opentelemetry import context
            from opentelemetry.baggage.propagation import W3CBaggagePropagator
            from opentelemetry.trace.propagation.tracecontext import (
                TraceContextTextMapPropagator,
            )
        except ImportError:
            context = None
            W3CBaggagePropagator = None
            TraceContextTextMapPropagator = None

        db2_connstr = os.environ.get("DB2_CONNSTR")
        if not db2_connstr:
            import config

        def connect_ibm_db(options=None):
            if db2_connstr:
                args = (db2_connstr, "", "")
            else:
                args = (config.database, config.user, config.password)
            if options is None:
                return ibm_db.connect(*args)
            return ibm_db.connect(*args, options)

        def connect_ibm_db_dbi(conn_options=None):
            if db2_connstr:
                args = (db2_connstr, "", "")
            else:
                args = (config.database, config.user, config.password)
            return ibm_db_dbi.connect(*args, conn_options=conn_options)

        try:
            probe = connect_ibm_db()
        except Exception:
            if db2_connstr:
                self.fail("Db2 connection failed using DB2_CONNSTR")
            self.skipTest("Db2 database connection is unavailable")
        else:
            ibm_db.close(probe)

        otel_attrs_supported = False
        conn = None
        try:
            conn = connect_ibm_db(OTEL_ATTRS)
        except Exception as error:
            self.assertIn(
                "clidriver used with ibm_db does not support OpenTelemetry",
                str(error),
            )
        else:
            self.assertTrue(conn)
            self.assertTrue(ibm_db.set_option(conn, OTEL_ATTRS, 1))
            for attr, expected in OTEL_ATTRS.items():
                self.assertEqual(ibm_db.get_option(conn, attr, 1), expected)
            otel_attrs_supported = True
        finally:
            if conn:
                ibm_db.close(conn)

        try:
            dbi_manual_conn = connect_ibm_db_dbi(
                conn_options=OTEL_ATTRS.copy()
            )
        except Exception as error:
            self.assertIn(
                "clidriver used with ibm_db does not support OpenTelemetry",
                str(error),
            )
        else:
            try:
                for attr, expected in OTEL_ATTRS.items():
                    self.assertEqual(dbi_manual_conn.get_option(attr), expected)
                otel_attrs_supported = True
            finally:
                dbi_manual_conn.close()

        conn = connect_ibm_db()
        self.assertTrue(conn)
        dbi_conn = connect_ibm_db_dbi()
        self.assertTrue(dbi_conn)
        self.assertTrue(dbi_conn.set_autocommit(True))
        token = None
        cursor = None
        try:
            if context is not None:
                headers = {
                    "traceparent": TRACEPARENT,
                    "tracestate": TRACESTATE,
                    "baggage": BAGGAGE,
                }
                otel_context = TraceContextTextMapPropagator().extract(headers)
                otel_context = W3CBaggagePropagator().extract(
                    headers, otel_context
                )
                token = context.attach(otel_context)

                context_conn = connect_ibm_db()
                try:
                    for attr, expected in OTEL_ATTRS.items():
                        actual = ibm_db.get_option(context_conn, attr, 1)
                        if otel_attrs_supported or actual is not False:
                            self.assertEqual(actual, expected)
                finally:
                    ibm_db.close(context_conn)

            stmt = ibm_db.exec_immediate(
                conn, "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1"
            )
            self.assertTrue(stmt)
            if context is not None:
                for attr, expected in OTEL_ATTRS.items():
                    actual = ibm_db.get_option(conn, attr, 1)
                    if otel_attrs_supported or actual is not False:
                        self.assertEqual(actual, expected)

            cursor = dbi_conn.cursor()
            cursor.execute("SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1")
            if context is not None:
                for attr, expected in OTEL_ATTRS.items():
                    actual = dbi_conn.get_option(attr)
                    if otel_attrs_supported or actual is not False:
                        self.assertEqual(actual, expected)

                context.detach(token)
                token = None
                updated_headers = {
                    "traceparent": UPDATED_TRACEPARENT,
                    "tracestate": UPDATED_TRACESTATE,
                    "baggage": UPDATED_BAGGAGE,
                }
                updated_context = TraceContextTextMapPropagator().extract(
                    updated_headers
                )
                updated_context = W3CBaggagePropagator().extract(
                    updated_headers, updated_context
                )
                token = context.attach(updated_context)

                stmt = ibm_db.exec_immediate(
                    conn, "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1"
                )
                self.assertTrue(stmt)
                for attr, expected in UPDATED_OTEL_ATTRS.items():
                    actual = ibm_db.get_option(conn, attr, 1)
                    if otel_attrs_supported or actual is not False:
                        self.assertEqual(actual, expected)

                cursor.execute(
                    "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1"
                )
                for attr, expected in UPDATED_OTEL_ATTRS.items():
                    actual = dbi_conn.get_option(attr)
                    if otel_attrs_supported or actual is not False:
                        self.assertEqual(actual, expected)

                transaction_conn = connect_ibm_db()
                transaction_stmt = None
                transaction_token = None
                try:
                    self.assertTrue(ibm_db.autocommit(transaction_conn, 0))
                    transaction_stmt = ibm_db.prepare(
                        transaction_conn,
                        "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1",
                    )
                    self.assertTrue(transaction_stmt)

                    def assert_transaction_attrs(expected_attrs):
                        for attr, expected in expected_attrs.items():
                            actual = ibm_db.get_option(transaction_conn, attr, 1)
                            if otel_attrs_supported or actual is not False:
                                self.assertEqual(actual, expected)

                    self.assertTrue(ibm_db.execute(transaction_stmt))
                    assert_transaction_attrs(UPDATED_OTEL_ATTRS)

                    transaction_context = TraceContextTextMapPropagator().extract(
                        headers
                    )
                    transaction_context = W3CBaggagePropagator().extract(
                        headers, transaction_context
                    )
                    transaction_token = context.attach(transaction_context)
                    stmt = ibm_db.exec_immediate(
                        transaction_conn,
                        "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1",
                    )
                    self.assertTrue(stmt)
                    ibm_db.free_result(stmt)
                    assert_transaction_attrs(UPDATED_OTEL_ATTRS)

                    self.assertTrue(ibm_db.commit(transaction_conn))
                    stmt = ibm_db.exec_immediate(
                        transaction_conn,
                        "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1",
                    )
                    self.assertTrue(stmt)
                    ibm_db.free_result(stmt)
                    assert_transaction_attrs(OTEL_ATTRS)

                    context.detach(transaction_token)
                    transaction_token = None
                    self.assertTrue(ibm_db.execute(transaction_stmt))
                    assert_transaction_attrs(OTEL_ATTRS)

                    self.assertTrue(ibm_db.rollback(transaction_conn))
                    stmt = ibm_db.exec_immediate(
                        transaction_conn,
                        "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1",
                    )
                    self.assertTrue(stmt)
                    ibm_db.free_result(stmt)
                    assert_transaction_attrs(UPDATED_OTEL_ATTRS)
                finally:
                    if transaction_token is not None:
                        context.detach(transaction_token)
                    if transaction_stmt is not None:
                        ibm_db.free_result(transaction_stmt)
                    ibm_db.close(transaction_conn)
        finally:
            if token is not None:
                context.detach(token)
            if cursor is not None:
                cursor.close()
            dbi_conn.close()
            ibm_db.close(conn)


if __name__ == "__main__":
    unittest.main()


#__END__
#__LUW_EXPECTED__
#test_331_OtelConnectionAttrs (test_331_OtelConnectionAttrs.IbmDbTestCase.test_331_OtelConnectionAttrs) ... ok
#__ZOS_EXPECTED__
#test_331_OtelConnectionAttrs (test_331_OtelConnectionAttrs.IbmDbTestCase.test_331_OtelConnectionAttrs) ... ok
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
