import asyncio
import pytest
from sanic import Sanic

def test_app_stop(app: Sanic):
    app.get("/")(lambda request: "Hello, World!")

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        await asyncio.sleep(0.1)  # Allow the server to start
        app.stop()

    app.run(host="127.0.0.1", port=42101, debug=False, single_process=True)

    assert app.is_running is False

def test_app_stop_with_error(app: Sanic):
    app.get("/")(lambda request: "Hello, World!")

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        await asyncio.sleep(0.1)  # Allow the server to start
        raise RuntimeError("Simulated error during stop")

    with pytest.raises(RuntimeError, match="Simulated error during stop"):
        app.run(host="127.0.0.1", port=42101, debug=False, single_process=True)

    assert app.is_running is False