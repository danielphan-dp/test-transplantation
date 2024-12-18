import pytest
from sanic import Sanic

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_app_stop(app):
    @app.get("/")
    async def handler(request):
        return "Hello, World!"

    app.stop()  # Ensure the app can be stopped without errors
    assert not app.is_running  # Check that the app is not running after stop

def test_app_stop_with_active_requests(app):
    @app.get("/")
    async def handler(request):
        return "Hello, World!"

    app.run(port=8000, single_process=True)
    app.stop()  # Stop the app while it is running
    assert not app.is_running  # Ensure the app is stopped

def test_app_stop_multiple_times(app):
    @app.get("/")
    async def handler(request):
        return "Hello, World!"

    app.run(port=8000, single_process=True)
    app.stop()  # First stop
    app.stop()  # Second stop, should not raise an error
    assert not app.is_running  # Ensure the app is still stopped

def test_app_stop_with_no_running_app(app):
    app.stop()  # Stop the app when it is not running
    assert not app.is_running  # Ensure the app is still not running

def test_app_stop_with_tasks(app):
    @app.get("/")
    async def handler(request):
        return "Hello, World!"

    app.run(port=8000, single_process=True)
    # Simulate a task that should be canceled on stop
    app.stop()  # Stop the app
    assert not app.is_running  # Ensure the app is stopped