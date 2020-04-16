import time
from os import getenv

import requests
from jaeger_client import Config
from opentracing_instrumentation.client_hooks import install_all_patches

JAEGER_HOST = getenv("JAEGER_HOST", "localhost")
WEBSERVER_HOST = getenv("WEBSERVER_HOST", "localhost")

# Create configuration object with enabled logging and sampling of all requests.
config = Config(
    config={"sampler": {"type": "const", "param": 1}, "logging": True, "local_agent": {"reporting_host": JAEGER_HOST}},
    service_name="jaeger_opentracing_example",
)
tracer = config.initialize_tracer()
install_all_patches()

url = "http://{}:8000/external-api".format(WEBSERVER_HOST)
# Make the actual request to webserver.
requests.get(url)

# allow tracer to flush the spans - https://github.com/jaegertracing/jaeger-client-python/issues/50
time.sleep(2)
tracer.close()
