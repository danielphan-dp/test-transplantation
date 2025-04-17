import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

def test_app_stop():
    app = Sanic(name="TestApp")

    @app.route("/")
    async def handler(request):
        return text("Hello, World!")

    @app.listener("after_server_start")
    async def after_start(app, loop):
        await asyncio.sleep(0.1)  # Simulate some processing
        app.stop()

    async def test_shutdown():
        await app.startup()
        assert app.is_running
        await app.shutdown()
        assert not app.is_running

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test_shutdown())
    loop.close()