import asyncio
import pytest
from sanic import Sanic
from sanic_testing.testing import HOST
from conftest import get_port

@pytest.mark.asyncio
async def test_start_stop_app(app):
    app_name = app.name
    output = []

    @app.after_server_start
    async def after_start(app):
        output.append(f"{app_name} started")

    @app.before_server_stop
    async def before_stop(app):
        output.append(f"{app_name} stopping")

    @app.after_server_stop
    async def after_stop(app):
        output.append(f"{app_name} stopped")

    await start_stop_app(app)

    assert output[0] == f"{app_name} started"
    assert output[1] == f"{app_name} stopping"
    assert output[2] == f"{app_name} stopped"

@pytest.mark.asyncio
async def test_start_stop_app_with_keyboard_interrupt(app):
    app_name = app.name
    output = []

    @app.after_server_start
    async def after_start(app):
        output.append(f"{app_name} started")
        await asyncio.sleep(1)  # Simulate some processing

    @app.before_server_stop
    async def before_stop(app):
        output.append(f"{app_name} stopping")

    @app.after_server_stop
    async def after_stop(app):
        output.append(f"{app_name} stopped")

    with pytest.raises(KeyboardInterrupt):
        await start_stop_app(app)

    assert output[0] == f"{app_name} started"
    assert output[1] == f"{app_name} stopping"
    assert output[2] == f"{app_name} stopped"