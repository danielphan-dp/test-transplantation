import asyncio
import pytest
from sanic import Sanic

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_app_stop(app):
    app.get("/")(lambda request: "Hello, World!")

    @app.listener("after_server_start")
    async def _start_listener(sanic, loop):
        await asyncio.sleep(0.1)  # Simulate some startup work
        app.stop()

    @app.listener("after_server_stop")
    async def _stop_listener(sanic, loop):
        assert not app.is_running

    app.run(host="127.0.0.1", port=42101, debug=False, single_process=True)
    assert not app.is_running

def test_app_stop_with_active_requests(app):
    app.get("/")(lambda request: "Hello, World!")

    @app.listener("after_server_start")
    async def _start_listener(sanic, loop):
        connect = asyncio.open_connection("127.0.0.1", 42101)
        reader, writer = await connect
        writer.write(b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n")
        await writer.drain()
        await asyncio.sleep(0.1)  # Allow time for the request to be processed
        app.stop()

    app.run(host="127.0.0.1", port=42101, debug=False, single_process=True)

def test_app_stop_with_no_requests(app):
    @app.listener("after_server_start")
    async def _start_listener(sanic, loop):
        await asyncio.sleep(0.1)  # Simulate some startup work
        app.stop()

    app.run(host="127.0.0.1", port=42101, debug=False, single_process=True)
    assert not app.is_running