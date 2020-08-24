from urllib.parse import urlunparse

import opentracing
from opentracing import InvalidCarrierException, SpanContextCorruptedException
from opentracing.ext import tags
from starlette.middleware.base import BaseHTTPMiddleware


class StarletteTracingMiddleWare(BaseHTTPMiddleware):
    def __init__(self, app, tracer):
        # Todo: add choice between global tracer and tracer that is already configured
        super().__init__(app)
        self._tracer = tracer

    async def dispatch(self, request, call_next):
        span_ctx = None
        headers = {}
        for k, v in request.headers.items():
            headers[k.lower()] = v

        try:
            span_ctx = self._tracer.extract(opentracing.Format.HTTP_HEADERS, headers)
        except (InvalidCarrierException, SpanContextCorruptedException):
            pass

        scope = request.scope
        with self._tracer.start_active_span(
            str(scope["path"]), child_of=span_ctx, finish_on_close=True
        ) as tracing_scope:
            span = tracing_scope.span
            span.set_tag(tags.COMPONENT, "asgi")
            span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
            span.set_tag(tags.HTTP_METHOD, scope["method"])
            host, port = scope["server"]
            url = urlunparse(
                (str(scope["scheme"]), f"{host}:{port}", str(scope["path"]), "", str(scope["query_string"]), "",)
            )
            span.set_tag(tags.HTTP_URL, url)

            response = await call_next(request)
        return response
