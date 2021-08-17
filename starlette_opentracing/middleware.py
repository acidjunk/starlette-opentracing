from urllib.parse import urlunparse

import opentracing
from opentracing import InvalidCarrierException, SpanContextCorruptedException
from opentracing.ext import tags
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class StarletteTracingMiddleWare(BaseHTTPMiddleware):
    def __init__(self, app, tracer, use_template: bool = False):
        # Todo: add choice between global tracer and tracer that is already configured
        super().__init__(app)
        self._tracer = tracer
        self.use_template = use_template

    def get_template(self, request: Request) -> str:
        """Get the template for the route endpoint."""
        method = request.method
        urls = [
            route
            for route in request.scope["router"].routes
            if hasattr(route, "endpoint") and
            "endpoint" in request.scope and
            route.endpoint == request.scope["endpoint"]
        ]
        template = urls[0].path if len(urls) > 0 else "UNKNOWN"
        method_path = method + " " + template
        return method_path

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

            if self.use_template:
                operation_name = self.get_template(request)
                span.set_operation_name(operation_name)
        return response
