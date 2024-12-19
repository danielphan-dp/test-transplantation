import asyncio
import pytest
from sanic import Sanic
from sanic_testing.testing import HOST
from conftest import get_port

@pytest.mark.asyncio
async def test_start_stop_app_with_shutdown(app):
    shutdown_called = False

    @app.after_server_start
    async def shutdown(app):
        nonlocal shutdown_called
        await asyncio.sleep(1.1)
        shutdown_called = True
        app.stop()

    app.run(HOST, get_port(), single_process=True)

    await asyncio.sleep(1.5)  # Wait for shutdown to be called
    assert shutdown_called

@pytest.mark.asyncio
async def test_start_stop_app_keyboard_interrupt(app):
    shutdown_called = False

    @app.after_server_start
    async def shutdown(app):
        nonlocal shutdown_called
        await asyncio.sleep(1.1)
        shutdown_called = True
        app.stop()

    try:
        app.run(HOST, get_port(), single_process=True)
    except KeyboardInterrupt:
        pass

    await asyncio.sleep(1.5)  # Wait for shutdown to be called
    assert shutdown_called

@pytest.mark.asyncio
async def test_start_stop_app_no_run_kwargs(app):
    shutdown_called = False

    @app.after_server_start
    async def shutdown(app):
        nonlocal shutdown_called
        await asyncio.sleep(1.1)
        shutdown_called = True
        app.stop()

    app.run(HOST, get_port(), single_process=True)

    await asyncio.sleep(1.5)  # Wait for shutdown to be called
    assert shutdown_called

@pytest.mark.asyncio
async def test_start_stop_app_with_run_kwargs(app):
    shutdown_called = False

    @app.after_server_start
    async def shutdown(app):
        nonlocal shutdown_called
        await asyncio.sleep(1.1)
        shutdown_called = True
        app.stop()

    app.run(HOST, get_port(), single_process=True, debug=True)

    await asyncio.sleep(1.5)  # Wait for shutdown to be called
    assert shutdown_called