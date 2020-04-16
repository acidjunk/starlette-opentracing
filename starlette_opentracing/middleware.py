from urllib.parse import urlunparse

import opentracing
from opentracing.ext import tags


# For now we use ASGI interface
# Todo: check if we can inherit from BaseHTTPMiddleware and/or opentracing.Tracer
class StarletteTracingMiddleWare:
    def __init__(self, app, tracer):
        # Todo: add choice between global tracer and tracer that is already configured
        # self.tracer = opentracing.global_tracer()
        self._tracer = tracer
        self.app = app

    async def __call__(self, scope, receive, send):
        # Skipping init for middle ware lifespan scope
        if scope["type"] == "lifespan":
            return

        # Skipping NON http events
        if scope["type"] not in ["http", "websocket"]:
            return

        # Try to find and existing context in the provided request headers
        span_ctx = None
        headers = {}
        for k, v in scope["headers"]:
            headers[k.lower().decode("utf-8")] = v.decode("utf-8")
        try:
            span_ctx = self._tracer.extract(opentracing.Format.HTTP_HEADERS, headers)
        except (opentracing.InvalidCarrierException, opentracing.SpanContextCorruptedException):
            pass

        with self._tracer.start_active_span(
            str(scope["path"]), child_of=span_ctx, finish_on_close=True
        ) as tracing_scope:
            span = tracing_scope.span
            span.set_tag(tags.COMPONENT, "asgi")
            span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
            if scope["type"] in {"http", "websocket"}:
                span.set_tag(tags.HTTP_METHOD, scope["method"])
                host, port = scope["server"]
                url = urlunparse(
                    (str(scope["scheme"]), f"{host}:{port}", str(scope["path"]), "", str(scope["query_string"]), "",)
                )
                span.set_tag(tags.HTTP_URL, url)
            await self.app(scope, receive, send)
            return
