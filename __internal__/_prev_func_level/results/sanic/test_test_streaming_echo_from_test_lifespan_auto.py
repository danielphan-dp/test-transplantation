import asyncio
import pytest
from sanic import Sanic

def test_app_stop():
    app = Sanic(name="TestApp")

    @app.route("/")
    async def handler(request):
        return "Hello, World!"

    async def test_stop():
        await app.stop()
        assert app.is_stopped

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test_stop())
    loop.close()

def test_app_stop_with_tasks():
    app = Sanic(name="TestAppWithTasks")
    shutdown_called = False

    @app.route("/")
    async def handler(request):
        return "Hello, World!"

    @app.listener("after_server_start")
    async def shutdown_task(app, loop):
        nonlocal shutdown_called
        await app.stop()
        shutdown_called = True

    async def test_stop_with_tasks():
        await app.stop()
        assert shutdown_called

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test_stop_with_tasks())
    loop.close()