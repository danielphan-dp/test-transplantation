import os
import pytest
from socket import AF_UNIX, socket
from sanic import Sanic

SOCKPATH = '/tmp/test.sock'
SOCKPATH2 = '/tmp/test2.sock'

@pytest.fixture
def app():
    app = Sanic(name="test")
    yield app

def test_stop_method(app):
    @app.after_server_start
    def stop(app: Sanic):
        app.stop()

    app.run(unix=SOCKPATH, single_process=True)
    assert not app.is_running

def test_stop_method_with_exception(app):
    @app.after_server_start
    def stop(app: Sanic):
        raise Exception("Forced stop")

    with pytest.raises(Exception, match="Forced stop"):
        app.run(unix=SOCKPATH, single_process=True)

def test_stop_method_multiple_starts(app):
    @app.after_server_start
    def stop(app: Sanic):
        app.stop()

    app.run(unix=SOCKPATH, single_process=True)
    assert not app.is_running

    with pytest.raises(FileExistsError):
        app.run(unix=SOCKPATH, single_process=True)

def test_stop_method_no_app_running(app):
    with pytest.raises(RuntimeError, match="Application is not running"):
        app.stop()