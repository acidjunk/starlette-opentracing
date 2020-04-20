from opentracing.mocktracer.tracer import MockTracer
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from starlette_opentracing.middleware import StarletteTracingMiddleWare


def test_tracer():
    app = Starlette()
    tracer = MockTracer()
    app.add_middleware(StarletteTracingMiddleWare, tracer=tracer)

    @app.route("/foo/")
    def foo(request):
        return PlainTextResponse("Foo")

    client = TestClient(app)
    client.get("/foo")
    spans = tracer.finished_spans()
    assert len(spans) == 2
    urls = [span.tags.get("http.url") for span in spans]
    assert "http://testserver:80/foo?b''" in urls
    # Todo: more asserts


def test_tracer_with_existing_context():
    app = Starlette()
    tracer = MockTracer()
    app.add_middleware(StarletteTracingMiddleWare, tracer=tracer)

    @app.route("/foo/")
    def foo(request):
        return PlainTextResponse("Foo")

    client = TestClient(app)
    client.get("/foo", headers={"Uber-Trace-Id": "floemp"})
    spans = tracer.finished_spans()
    urls = [span.tags.get("http.url") for span in spans]
    assert "http://testserver:80/foo?b''" in urls
    # Todo: fix test that also hits the extra header part in the middleware
    # assert len(spans) == 3
    # Todo: more asserts
