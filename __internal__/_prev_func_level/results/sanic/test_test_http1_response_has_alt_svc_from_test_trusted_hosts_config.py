import sys
import pytest
from pathlib import Path
from sanic import Sanic
from sanic.response import text, empty
from tests.client import RawClient

@pytest.mark.skipif(sys.version_info < (3, 9), reason='Not supported in 3.7')
def test_get_method_response(port):
    Sanic._app_registry.clear()
    app = Sanic("TestGetMethod")
    response = b""

    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    @app.after_server_start
    async def do_request(*_):
        nonlocal response

        app.router.reset()
        app.router.finalize()

        client = RawClient(app.state.host, app.state.port)
        await client.connect()
        await client.send(
            """
            GET /get HTTP/1.1
            host: localhost:7777

            """
        )
        response = await client.recv(1024)
        await client.close()

    @app.after_server_start
    def shutdown(*_):
        app.stop()

    app.prepare(version=1, port=port)
    Sanic.serve_single(app)

    assert b'I am get method' in response

def test_get_method_invalid_route(port):
    Sanic._app_registry.clear()
    app = Sanic("TestGetMethodInvalidRoute")
    response = b""

    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    @app.after_server_start
    async def do_request(*_):
        nonlocal response

        app.router.reset()
        app.router.finalize()

        client = RawClient(app.state.host, app.state.port)
        await client.connect()
        await client.send(
            """
            GET /invalid HTTP/1.1
            host: localhost:7777

            """
        )
        response = await client.recv(1024)
        await client.close()

    @app.after_server_start
    def shutdown(*_):
        app.stop()

    app.prepare(version=1, port=port)
    Sanic.serve_single(app)

    assert b'404 Not Found' in response

def test_get_method_with_query_params(port):
    Sanic._app_registry.clear()
    app = Sanic("TestGetMethodWithQueryParams")
    response = b""

    @app.get("/get")
    async def handler(request):
        return text(f'I am get method with param: {request.args.get("param", "None")}')

    @app.after_server_start
    async def do_request(*_):
        nonlocal response

        app.router.reset()
        app.router.finalize()

        client = RawClient(app.state.host, app.state.port)
        await client.connect()
        await client.send(
            """
            GET /get?param=test HTTP/1.1
            host: localhost:7777

            """
        )
        response = await client.recv(1024)
        await client.close()

    @app.after_server_start
    def shutdown(*_):
        app.stop()

    app.prepare(version=1, port=port)
    Sanic.serve_single(app)

    assert b'I am get method with param: test' in response