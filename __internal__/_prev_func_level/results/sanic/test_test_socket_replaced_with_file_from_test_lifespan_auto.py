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
    assert not app.is_running

def test_app_stop_with_exception(app):
    @app.after_server_start
    async def after_start(app: Sanic):
        raise SanicException("Forced shutdown")

    with pytest.raises(SanicException, match="Forced shutdown"):
        app.run(host="myhost.invalid", single_process=True)

def test_app_stop_multiple_calls(app):
    @app.after_server_start
    async def after_start(app: Sanic):
        app.stop()
        app.stop()  # Calling stop again to check for idempotency

    app.run(host="myhost.invalid", single_process=True)
    assert not app.is_running

def test_app_stop_no_running(app):
    with pytest.raises(RuntimeError, match="Cannot stop a non-running application"):
        app.stop()