import sys
import pytest
from pathlib import Path
from sanic import Sanic
from sanic.response import text
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

    assert response.decode() == "I am get method"