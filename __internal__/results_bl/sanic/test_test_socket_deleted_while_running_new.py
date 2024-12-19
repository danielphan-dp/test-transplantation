import os
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

SOCKPATH = '/tmp/test.sock'

@pytest.fixture
def app():
    app = Sanic(name="test")
    yield app

def test_stop_method_stops_app(app):
    @app.after_server_start
    async def after_start(app: Sanic):
        app.stop()

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)

def test_stop_method_when_not_running(app):
    with pytest.raises(SanicException):
        app.stop()

def test_stop_method_multiple_calls(app):
    @app.after_server_start
    async def after_start(app: Sanic):
        app.stop()
        app.stop()  # Calling stop again

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)

def test_stop_method_with_cleanup(app):
    @app.after_server_start
    async def after_start(app: Sanic):
        os.unlink(SOCKPATH)
        app.stop()

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)
    assert not os.path.exists(SOCKPATH)  # Ensure socket is deleted

def test_stop_method_with_no_socket(app):
    @app.after_server_start
    async def after_start(app: Sanic):
        if os.path.exists(SOCKPATH):
            os.unlink(SOCKPATH)
        app.stop()

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)