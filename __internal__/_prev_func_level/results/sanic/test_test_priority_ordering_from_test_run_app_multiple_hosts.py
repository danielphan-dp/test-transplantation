import asyncio
import signal
import pytest
from sanic import Sanic, Blueprint
from sanic_testing.testing import HOST
from conftest import get_port

@pytest.mark.asyncio
async def test_start_stop_app(app):
    output = []
    app = Sanic("TestApp")

    @app.after_server_start
    async def after_start(app):
        output.append("after_start")

    @app.before_server_stop
    async def before_stop(app):
        output.append("before_stop")

    @app.listener("after_server_stop")
    async def after_stop(app):
        output.append("after_stop")

    @app.listener("before_server_start")
    async def before_start(app):
        output.append("before_start")

    app.run(HOST, get_port(), single_process=True)

    await asyncio.sleep(1.5)  # Allow time for the app to start and stop

    assert "after_start" in output
    assert "before_stop" in output
    assert "after_stop" in output
    assert "before_start" in output

@pytest.mark.asyncio
async def test_start_stop_app_keyboard_interrupt(app):
    output = []
    app = Sanic("TestApp")

    @app.after_server_start
    async def after_start(app):
        output.append("after_start")

    @app.before_server_stop
    async def before_stop(app):
        output.append("before_stop")

    signal.signal(signal.SIGINT, lambda s, f: app.stop())

    app.run(HOST, get_port(), single_process=True)

    await asyncio.sleep(1.5)  # Allow time for the app to start and stop

    assert "after_start" in output
    assert "before_stop" in output

@pytest.mark.asyncio
async def test_start_stop_app_multiple_runs(app):
    output = []
    app = Sanic("TestApp")

    @app.after_server_start
    async def after_start(app):
        output.append("after_start")

    @app.before_server_stop
    async def before_stop(app):
        output.append("before_stop")

    for _ in range(3):
        app.run(HOST, get_port(), single_process=True)
        await asyncio.sleep(1.5)  # Allow time for the app to start and stop

    assert output.count("after_start") == 3
    assert output.count("before_stop") == 3