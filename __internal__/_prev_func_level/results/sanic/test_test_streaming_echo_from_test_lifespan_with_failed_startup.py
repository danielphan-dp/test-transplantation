import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_app_stop(app):
    """Test stopping the Sanic app."""
    
    @app.route("/")
    async def handler(request):
        return text("Hello, World!")

    @app.listener("after_server_start")
    async def after_start(app, loop):
        await asyncio.sleep(0.1)  # Simulate some processing
        app.stop()

    @app.listener("before_server_stop")
    async def before_stop(app, loop):
        assert app.is_running  # Ensure the app is running before stopping

    app.run(access_log=False, single_process=True)

    assert not app.is_running  # Ensure the app has stopped

def test_app_stop_with_error_handling(app):
    """Test stopping the Sanic app with error handling."""
    
    @app.route("/")
    async def handler(request):
        return text("Hello, World!")

    @app.listener("after_server_start")
    async def after_start(app, loop):
        await asyncio.sleep(0.1)  # Simulate some processing
        try:
            app.stop()
        except Exception as e:
            assert str(e) == "Expected error message"  # Replace with actual expected error

    app.run(access_log=False, single_process=True)

    assert not app.is_running  # Ensure the app has stopped

def test_app_stop_multiple_times(app):
    """Test stopping the Sanic app multiple times."""
    
    @app.route("/")
    async def handler(request):
        return text("Hello, World!")

    @app.listener("after_server_start")
    async def after_start(app, loop):
        await asyncio.sleep(0.1)  # Simulate some processing
        app.stop()
        app.stop()  # Attempt to stop again

    app.run(access_log=False, single_process=True)

    assert not app.is_running  # Ensure the app has stopped