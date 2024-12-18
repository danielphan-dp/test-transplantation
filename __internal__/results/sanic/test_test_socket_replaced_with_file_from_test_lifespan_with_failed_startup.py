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

def test_app_stop_with_exception(app):
    @app.after_server_start
    async def after_start(app: Sanic):
        raise RuntimeError("Forced exception during startup")
    
    with pytest.raises(RuntimeError, match="Forced exception during startup"):
        app.run(host="myhost.invalid", single_process=True)

def test_app_stop_no_running_server(app):
    with pytest.raises(SanicException, match="Cannot stop a server that is not running"):
        app.stop()