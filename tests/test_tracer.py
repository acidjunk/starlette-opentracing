import opentracing
from opentracing.mocktracer.tracer import MockTracer
from opentracing.scope_managers.contextvars import ContextVarsScopeManager
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from starlette_opentracing.middleware import StarletteTracingMiddleWare


def test_tracer():
    app = Starlette()
    mocked_tracer = MockTracer()
    app.add_middleware(StarletteTracingMiddleWare, tracer=mocked_tracer)

    @app.route("/foo/")
    def foo(request):
        return PlainTextResponse("Foo")

    client = TestClient(app)
    client.get("/foo")
    spans = mocked_tracer.finished_spans()
    assert len(spans) == 2
    urls = [span.tags.get("http.url") for span in spans]
    assert "http://testserver:80/foo?b''" in urls
    # Todo: more asserts


def test_tracer_with_extra_context():
    app = Starlette()
    mocked_tracer = MockTracer(scope_manager=ContextVarsScopeManager())

    app.add_middleware(StarletteTracingMiddleWare, tracer=mocked_tracer)

    @app.route("/foo/")
    def foo(request):
        return PlainTextResponse("Foo")

    external_tracer = MockTracer(scope_manager=ContextVarsScopeManager())
    external_tracer.start_active_span("EXTERNAL")

    # Prepare headers
    headers = {}
    external_tracer.inject(external_tracer.active_span.context, opentracing.Format.TEXT_MAP, headers)
    client = TestClient(app)
    client.get("/foo", headers=headers)

    external_tracer.active_span.finish()

    spans = mocked_tracer.finished_spans()
    assert len(spans) == 2
    urls = [span.tags.get("http.url") for span in spans]
    assert "http://testserver:80/foo?b''" in urls

    # Todo: more asserts; still not sure if we should have 3 finished spans in the external tracer
    spans = external_tracer.finished_spans()
    assert len(spans) == 1


def test_tracer_uses_path_templates_for_operation_names():
    app = Starlette()
    mocked_tracer = MockTracer(scope_manager=ContextVarsScopeManager())
    app.add_middleware(
        StarletteTracingMiddleWare, tracer=mocked_tracer, use_template=True
    )

    @app.route("/foo/{foo_id}")
    def foo(foo_id: str):
        return PlainTextResponse(f"Foo: {foo_id}")

    client = TestClient(app)
    client.get("/foo/MyFoo")
    spans = mocked_tracer.finished_spans()
    assert len(spans) == 1
    assert spans[0].operation_name == "GET /foo/{foo_id}"


def test_tracer_uses_set_template_to_unknown_if_no_endpoint():
    app = Starlette()
    mocked_tracer = MockTracer(scope_manager=ContextVarsScopeManager())
    app.add_middleware(
        StarletteTracingMiddleWare, tracer=mocked_tracer, use_template=True
    )

    @app.route("/foo/{foo_id}")
    def foo(foo_id: str):
        return PlainTextResponse(f"Foo: {foo_id}")

    client = TestClient(app)
    client.get("/bar/MyFoo")
    spans = mocked_tracer.finished_spans()
    assert len(spans) == 1
    assert spans[0].operation_name == "GET UNKNOWN"
