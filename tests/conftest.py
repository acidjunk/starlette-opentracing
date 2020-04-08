import pytest
from opentracing.mocktracer import MockTracer
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from starlette_opentracing import StarletteTracingMiddleWare


# Todo: scope might be bigger
@pytest.fixture()
def app():
    app_ = Starlette()
    app_.add_middleware(StarletteTracingMiddleWare, tracer=MockTracer())

    @app_.route("/foo/")
    def foo(request):
        return PlainTextResponse("Foo")

    @app_.route("/bar/")
    def bar(request):
        raise ValueError("bar")

    @app_.route("/foo/{bar}/")
    def foobar(request):
        return PlainTextResponse(f"Foo: {request.path_params['bar']}")

    return app_


@pytest.fixture
def client(app):
    return TestClient(app)
