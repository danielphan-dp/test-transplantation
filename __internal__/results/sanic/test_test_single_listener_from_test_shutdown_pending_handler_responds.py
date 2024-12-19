import asyncio
import pytest
from sanic import Sanic
from sanic_testing.testing import HOST
from conftest import get_port

@pytest.mark.asyncio
async def test_start_stop_app(app):
    """Test that the start_stop_app function correctly starts and stops the app."""
    output = []
    app.listener("after_server_start")(create_listener("after_server_start", output))
    
    # Start the app
    await asyncio.sleep(0.5)  # Allow some time for the app to start
    start_stop_app(app)

    # Check if the app has started and the listener was called
    assert app.name + "after_server_start" == output.pop()

    # Ensure the app is stopped after the shutdown
    await asyncio.sleep(1.5)  # Wait for the shutdown to complete
    assert app.is_stopped

@pytest.mark.parametrize("listener_name", ["before_server_stop", "after_server_stop"])
@pytest.mark.asyncio
async def test_multiple_listeners(app, listener_name):
    """Test that multiple listeners can be registered and triggered correctly."""
    output = []
    app.listener(listener_name)(create_listener(listener_name, output))
    
    start_stop_app(app)
    
    assert app.name + listener_name == output.pop()

async def create_listener(name, output):
    """Simulate a listener that appends its name to the output."""
    await asyncio.sleep(0.1)
    output.append(name)