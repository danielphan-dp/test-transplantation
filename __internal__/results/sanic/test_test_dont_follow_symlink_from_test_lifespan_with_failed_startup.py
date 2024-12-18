import os
import pytest
from sanic import Sanic
from socket import AF_UNIX, socket

SOCKPATH = "/tmp/sanic.sock"
SOCKPATH2 = "/tmp/sanic2.sock"

@pytest.fixture
def app():
    app = Sanic(name="test_app")
    yield app

def test_stop_method(app):
    @app.after_server_start
    def after_start(app: Sanic):
        app.stop()

    with pytest.raises(SystemExit):
        app.run(unix=SOCKPATH, single_process=True)

def test_stop_method_with_symlink(app):
    with socket(AF_UNIX) as sock:
        sock.bind(SOCKPATH2)
    os.symlink(SOCKPATH2, SOCKPATH)

    @app.after_server_start
    def after_start(app: Sanic):
        app.stop()

    with pytest.raises(FileExistsError):
        app.run(unix=SOCKPATH, single_process=True)

def test_stop_method_without_start(app):
    with pytest.raises(RuntimeError):
        app.stop()