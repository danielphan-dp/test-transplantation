import asyncio
from sanic import Sanic
import pytest

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_stop_method(app: Sanic):
    app.get("/")(lambda request: "Hello, World!")

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        await asyncio.sleep(0.1)  # Allow server to start
        app.stop()

    app.run(host="127.0.0.1", port=42101, debug=False, single_process=True)

def test_stop_method_no_running_app(app: Sanic):
    with pytest.raises(RuntimeError):
        app.stop()