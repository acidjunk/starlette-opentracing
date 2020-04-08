import requests
from starlette.applications import Starlette
from starlette.responses import JSONResponse

from jaeger_client import Config as jaeger_config
from opentracing_instrumentation.client_hooks import install_all_patches
from starlette_opentracing import StarletteTracingMiddleWare


import uvicorn


app = Starlette(debug=True)

@app.route('/')
async def homepage(request):
    return JSONResponse({'title': 'Home', 'content': 'Home content'})


@app.route('/external-api')
def call_external_api(request):
    # Note: Using requests instead of httpx here so you can see the effect of `install_all_patches()`
    try:
        r = requests.get('https://api.github.com/events')
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return JSONResponse({'title': 'Call external API', 'content': {"error": str(err)}})
    return JSONResponse({'title': 'Call external API', 'content': r.json()})


@app.exception_handler(404)
async def not_found(r, exc):
    context = {"method": r.method, "client": r.client, "url": r.url.path, "query_params": {**r.query_params}}
    response = {'title': 'Page not found', 'content': 'Page not found', 'context':{**context}}
    return JSONResponse(response, status_code=404)



opentracing_config = jaeger_config(
    config={
        "sampler": {"type": "const", "param": 1},
        "logging": False,
        "local_agent": {"reporting_host": "localhost"},
    },
    service_name="Starlette tracer example",
)
jaeger_tracer = opentracing_config.initialize_tracer()
install_all_patches()
app.add_middleware(StarletteTracingMiddleWare, tracer=jaeger_tracer)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)