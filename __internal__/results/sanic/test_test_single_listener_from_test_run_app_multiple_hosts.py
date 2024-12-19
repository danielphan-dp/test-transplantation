import asyncio
import pytest
from sanic import Sanic
from sanic_testing.testing import HOST
from conftest import get_port

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
@pytest.mark.asyncio
async def test_start_stop_app_with_listener(app, listener_name):
    """Test that the start_stop_app method works with a listener"""
    output = []
    
    @app.listener(listener_name)
    async def create_listener(name, output):
        output.append(app.name + name)

    await start_stop_app(app)
    
    assert output, "Output should not be empty"
    assert app.name + listener_name == output.pop()

@pytest.mark.asyncio
async def test_start_stop_app_keyboard_interrupt(app):
    """Test that start_stop_app handles KeyboardInterrupt gracefully"""
    async def shutdown(app):
        await asyncio.sleep(1.1)
        app.stop()

    app.after_server_start(shutdown)
    
    try:
        await start_stop_app(app)
    except KeyboardInterrupt:
        pass
    assert not app.is_running, "App should not be running after shutdown"