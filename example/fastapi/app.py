import requests
import uvicorn
from fastapi import FastAPI
from jaeger_client import Config as jaeger_config
from opentracing_instrumentation.client_hooks import install_all_patches

from starlette_opentracing import StarletteTracingMiddleWare

app = FastAPI()


@app.get("/")
async def homepage():
    return {"title": "Home", "content": "Home content"}


@app.get("/external-api")
def call_external_api():
    # Note: Using requests instead of httpx here so you can see the effect of `install_all_patches()`
    try:
        r = requests.get("https://api.github.com/events")
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {"title": "Call external API", "content": {"error": str(err)}}
    return {"title": "Call external API", "content": r.json()}


opentracing_config = jaeger_config(
    config={
        "sampler": {"type": "const", "param": 1},
        "logging": False,
        "local_agent": {"reporting_host": "localhost"},
    },
    service_name="FastAPI tracer example",
)
jaeger_tracer = opentracing_config.initialize_tracer()
install_all_patches()
app.add_middleware(StarletteTracingMiddleWare, tracer=jaeger_tracer)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
