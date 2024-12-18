import os
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic(name="test_app")
    yield app

def test_app_stop(app):
    @app.after_server_start
    async def after_start(app: Sanic):
        app.stop()

    app.run(host="myhost.invalid", single_process=True)

def test_app_stop_with_error(app):
    @app.after_server_start
    async def after_start_with_error(app: Sanic):
        raise RuntimeError("Simulated error during startup")
    
    with pytest.raises(RuntimeError, match="Simulated error during startup"):
        app.run(host="myhost.invalid", single_process=True)

def test_app_stop_multiple_calls(app):
    @app.after_server_start
    async def after_start_multiple(app: Sanic):
        app.stop()
        app.stop()  # Calling stop again to check for exceptions

    app.run(host="myhost.invalid", single_process=True)

def test_app_stop_no_running_server(app):
    with pytest.raises(SanicException, match="Cannot stop a server that is not running"):
        app.stop()