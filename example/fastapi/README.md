# FastAPI opentracing example

An example of using the middleware with FastAPI and instrumentation for some commonly used python libs for DB access
and external http requests. Using the `install_all_patches()` method from `opentracing_instrumentation` package gives
you a way to trace your MySQLdb, SQLAlchemy, Redis queries and more without writing boilerplate code.

It uses a local running `jaeger` instance as a tracing system. You can install `jaeger` for your OS with the info on
https://www.jaegertracing.io/download/ or start a self contained dockerized variant with:

```
docker run -d -e \
  COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 9411:9411 \
  jaegertracing/all-in-one:latest
```

When `jaeger` is up and running you can access it at: http://localhost:16686/search

Now install the requirements and start FastAPI:

```bash
python3 -m venv example
source example/bin/activate
pip install -r requirements.txt
python app.py
```

When you access the following URL's, you should see the traces in the Jaeger WebGUI:

http://localhost:8000/

http://localhost:8000/external-api

http://localhost:8000/test-404

You can also use the client.py to setup a tracing session before doing a request: the middleware will add the other
request to the existing span:

```
python app.py
```
