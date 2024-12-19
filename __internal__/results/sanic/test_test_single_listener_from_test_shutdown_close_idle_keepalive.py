import asyncio
import pytest
from sanic import Sanic
from sanic_testing.testing import HOST
from conftest import get_port

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
async def test_start_stop_app_with_listener(app, listener_name):
    """Test that start_stop_app correctly starts and stops the app with a listener."""
    output = []
    
    @app.listener(listener_name)
    async def create_listener(name, output):
        output.append(app.name + name)

    async def run_test():
        await asyncio.sleep(1)
        assert output, "Output should not be empty after app run"
        assert app.name + listener_name == output.pop()

    app.after_server_start(run_test)
    await start_stop_app(app)
    
    assert app.is_running is False, "App should not be running after stop"
    
@pytest.mark.asyncio
async def test_start_stop_app_with_no_listener(app):
    """Test that start_stop_app works without any listeners."""
    output = []

    async def run_test():
        await asyncio.sleep(1)
        output.append("No listener triggered")

    app.after_server_start(run_test)
    await start_stop_app(app)

    assert app.is_running is False, "App should not be running after stop"
    assert output == ["No listener triggered"], "Output should match expected value"