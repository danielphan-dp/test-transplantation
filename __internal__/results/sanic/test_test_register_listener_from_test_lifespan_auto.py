import asyncio
import pytest
from sanic_testing.testing import HOST
from sanic import Sanic
from conftest import get_port

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
async def test_register_listener_with_shutdown(app, listener_name):
    """
    Test that listeners work with app.register_listener method and ensure
    the app shuts down correctly after the listener is triggered.
    """
    output = []
    
    async def shutdown_listener(app):
        await asyncio.sleep(1.1)
        output.append(app.name + listener_name)
        app.stop()

    app.register_listener(shutdown_listener, event='after_server_start')
    
    try:
        app.run(HOST, get_port(), single_process=True)
    except KeyboardInterrupt:
        pass

    assert output
    assert app.name + listener_name == output.pop()

@pytest.mark.asyncio
async def test_register_listener_without_shutdown(app):
    """
    Test that the app can register a listener without triggering shutdown.
    """
    output = []
    
    async def no_shutdown_listener(app):
        output.append("Listener executed without shutdown")

    app.register_listener(no_shutdown_listener, event='after_server_start')
    
    app.run(HOST, get_port(), single_process=True)

    assert output
    assert "Listener executed without shutdown" in output

@pytest.mark.asyncio
async def test_register_multiple_listeners(app):
    """
    Test that multiple listeners can be registered and executed in order.
    """
    output = []

    async def first_listener(app):
        output.append("First listener executed")

    async def second_listener(app):
        output.append("Second listener executed")
        app.stop()

    app.register_listener(first_listener, event='after_server_start')
    app.register_listener(second_listener, event='after_server_start')

    try:
        app.run(HOST, get_port(), single_process=True)
    except KeyboardInterrupt:
        pass

    assert output
    assert output[0] == "First listener executed"
    assert output[1] == "Second listener executed"