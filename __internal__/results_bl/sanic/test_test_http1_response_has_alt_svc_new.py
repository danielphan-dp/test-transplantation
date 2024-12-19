import sys
import pytest
from pathlib import Path
from sanic.app import Sanic
from sanic.response import empty
from tests.client import RawClient

@pytest.mark.skipif(sys.version_info < (3, 9), reason='Not supported in 3.7')
def test_stop_method_stops_app(port):
    app = Sanic("TestStopMethod")
    app.config.TOUCHUP = True

    @app.get("/")
    async def handler(*_):
        return empty()

    @app.after_server_start
    async def do_request(*_):
        client = RawClient(app.state.host, app.state.port)
        await client.connect()
        await client.send(
            """
            GET / HTTP/1.1
            host: localhost:7777

            """
        )
        response = await client.recv(1024)
        await client.close()
        return response

    app.prepare(port=port)
    Sanic.serve_single(app)

    app.stop()
    assert app.is_stopped

@pytest.mark.skipif(sys.version_info < (3, 9), reason='Not supported in 3.7')
def test_stop_method_when_not_running(port):
    app = Sanic("TestStopWhenNotRunning")
    app.stop()
    assert app.is_stopped

@pytest.mark.skipif(sys.version_info < (3, 9), reason='Not supported in 3.7')
def test_stop_method_multiple_calls(port):
    app = Sanic("TestMultipleStops")
    app.prepare(port=port)
    app.stop()
    assert app.is_stopped
    app.stop()
    assert app.is_stopped