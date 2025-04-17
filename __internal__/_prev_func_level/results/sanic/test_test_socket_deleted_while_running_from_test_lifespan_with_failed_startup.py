import os
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

SOCKPATH = "/tmp/test.sock"

@pytest.fixture
def app():
    app = Sanic(name="test")
    yield app

def test_stop_method_stops_app(app):
    @app.after_server_start
    async def after_start(app: Sanic):
        app.stop()

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)
    assert not app.is_running

def test_stop_method_when_not_running(app):
    with pytest.raises(SanicException, match="Application is not running"):
        app.stop()

def test_stop_method_multiple_calls(app):
    @app.after_server_start
    async def after_start(app: Sanic):
        app.stop()
        app.stop()  # Calling stop again

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)
    assert not app.is_running

def test_stop_method_with_cleanup(app):
    cleanup_called = False

    @app.after_server_start
    async def after_start(app: Sanic):
        nonlocal cleanup_called
        app.stop()
        cleanup_called = True

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)
    assert cleanup_called

def test_stop_method_with_socket_deleted(app):
    @app.after_server_start
    async def after_start(app: Sanic):
        os.unlink(SOCKPATH)
        app.stop()

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)
    assert not app.is_running
    assert not os.path.exists(SOCKPATH)