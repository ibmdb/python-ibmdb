"""OpenTelemetry context extraction and ibm_db connection attribute updates."""

_OTEL_ATTRIBUTES = (
    ("traceparent", "SQL_ATTR_OTEL_TRACEPARENT", 0x01),
    ("tracestate", "SQL_ATTR_OTEL_TRACESTATE", 0x02),
    ("baggage", "SQL_ATTR_OTEL_BAGGAGE", 0x04),
)


def _current_context_headers():
    try:
        from opentelemetry.baggage.propagation import W3CBaggagePropagator
        from opentelemetry.trace.propagation.tracecontext import (
            TraceContextTextMapPropagator,
        )
    except ImportError:
        return {}

    headers = {}
    TraceContextTextMapPropagator().inject(headers)
    W3CBaggagePropagator().inject(headers)
    return headers


def apply_otel_context(connection, explicit_attrs=(), clear_attrs=()):
    """Set current W3C context on a connection using ibm_db.set_option.

    Returns the bit mask of automatically populated attributes, or None when
    the CLI driver does not support the OTEL connection attributes.
    """
    import ibm_db

    headers = _current_context_headers()
    explicit_attrs = set(explicit_attrs)
    clear_attrs = set(clear_attrs)
    options = {}
    active_mask = 0

    for header, attr_name, bit in _OTEL_ATTRIBUTES:
        attr = getattr(ibm_db, attr_name)
        if attr in explicit_attrs:
            continue
        value = headers.get(header)
        if value:
            options[attr] = value
            active_mask |= bit
        elif attr in clear_attrs:
            options[attr] = ""

    if not options:
        return active_mask

    try:
        result = ibm_db.set_option(connection, options, 1)
    except Exception as error:
        if "does not support OpenTelemetry connection attributes" in str(error):
            return None
        raise

    if not result:
        raise RuntimeError("ibm_db.set_option failed to set OpenTelemetry attributes")
    return active_mask
