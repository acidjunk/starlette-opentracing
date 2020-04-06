from urllib.parse import urlunparse

import opentracing
from opentracing.ext import tags


# Todo: check if we can inherit from BaseHTTPMiddleware and/or opentracing.Tracer
# For now we use ASGI interface
class StarletteTracingMiddleWare:
    def __init__(self, app, tracer):
        # Todo: add choice etween global tracer and tracer that is already configured
        # self.tracer = opentracing.global_tracer()
        self.tracer = tracer
        self.app = app

    async def __call__(self, scope, receive, send):
        with self.tracer.start_active_span("request") as tracing_scope:
            span = tracing_scope.span
            span.set_tag(tags.COMPONENT, "asgi")
            span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
            if scope["type"] in {"http", "websocket"}:
                span.set_tag(tags.HTTP_METHOD, scope["method"])
                host, port = scope["server"]
                # url = urlunparse((scope["scheme"], f"{host}:{port}", scope["path"], "", scope["query_string"], "",))
                url = "http://www.FIXME.com"
                span.set_tag(tags.HTTP_URL, url)
            await self.app(scope, receive, send)
