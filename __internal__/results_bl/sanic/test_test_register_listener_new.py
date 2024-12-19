import asyncio
import pytest
from sanic_testing.testing import HOST
from conftest import get_port

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
async def test_register_listener_with_shutdown(app, listener_name):
    """
    Test that listeners work with app.register_listener method
    and that the app shuts down properly after starting.
    """
    output = []
    listener = create_listener(listener_name, output)
    app.register_listener(listener, event=listener_name)
    
    # Start the app and wait for it to shut down
    await asyncio.sleep(0.5)  # Allow some time for the app to start
    start_stop_app(app)
    
    assert app.name + listener_name == output.pop()

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
async def test_register_listener_with_keyboard_interrupt(app, listener_name):
    """
    Test that the app can handle a KeyboardInterrupt during startup.
    """
    output = []
    listener = create_listener(listener_name, output)
    app.register_listener(listener, event=listener_name)
    
    # Simulate a KeyboardInterrupt
    with pytest.raises(KeyboardInterrupt):
        start_stop_app(app, run_kwargs={'debug': True})  # Pass debug to trigger KeyboardInterrupt

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
async def test_register_listener_with_invalid_listener(app, listener_name):
    """
    Test that registering an invalid listener raises an exception.
    """
    output = []
    invalid_listener = "invalid_listener"
    
    with pytest.raises(Exception):
        app.register_listener(invalid_listener, event=listener_name)
        start_stop_app(app)