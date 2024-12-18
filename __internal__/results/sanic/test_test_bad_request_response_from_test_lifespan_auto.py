import asyncio
import pytest
from sanic import Sanic

def test_app_stop(app: Sanic):
    app_started = False
    app_stopped = False

    @app.listener("after_server_start")
    async def start_listener(sanic, loop):
        nonlocal app_started
        app_started = True

    @app.listener("after_server_stop")
    async def stop_listener(sanic, loop):
        nonlocal app_stopped
        app_stopped = True

    app.run(host="127.0.0.1", port=42101, debug=False, single_process=True)
    assert app_started
    app.stop()
    assert app_stopped

def test_app_stop_no_listener(app: Sanic):
    app_stopped = False

    @app.listener("after_server_stop")
    async def stop_listener(sanic, loop):
        nonlocal app_stopped
        app_stopped = True

    app.run(host="127.0.0.1", port=42101, debug=False, single_process=True)
    app.stop()
    assert app_stopped

def test_app_stop_multiple_stops(app: Sanic):
    stop_count = 0

    @app.listener("after_server_stop")
    async def stop_listener(sanic, loop):
        nonlocal stop_count
        stop_count += 1

    app.run(host="127.0.0.1", port=42101, debug=False, single_process=True)
    app.stop()
    app.stop()
    assert stop_count == 1

def test_app_stop_with_tasks(app: Sanic):
    task_completed = False

    @app.route("/")
    async def handler(request):
        return "Hello, World!"

    @app.listener("after_server_start")
    async def start_listener(sanic, loop):
        await asyncio.sleep(0.1)  # Simulate some task
        nonlocal task_completed
        task_completed = True

    app.run(host="127.0.0.1", port=42101, debug=False, single_process=True)
    app.stop()
    assert task_completed