import os
import pytest
from sanic import Sanic
from socket import AF_UNIX, socket

SOCKPATH = "/tmp/sockpath"
SOCKPATH2 = "/tmp/sockpath2"

def test_stop_app():
    app = Sanic(name="test_stop_app")

    @app.after_server_start
    def after_start(app: Sanic):
        app.stop()

    with pytest.raises(RuntimeError):
        app.run(unix=SOCKPATH, single_process=True)

def test_stop_app_with_symlink():
    with socket(AF_UNIX) as sock:
        sock.bind(SOCKPATH2)
    os.symlink(SOCKPATH2, SOCKPATH)

    app = Sanic(name="test_stop_app_with_symlink")

    @app.after_server_start
    def after_start(app: Sanic):
        app.stop()

    with pytest.raises(FileExistsError):
        app.run(unix=SOCKPATH, single_process=True)

def test_stop_app_multiple_starts():
    app = Sanic(name="test_stop_app_multiple_starts")

    @app.after_server_start
    def after_start(app: Sanic):
        app.stop()

    app.run(single_process=True)
    with pytest.raises(RuntimeError):
        app.run(single_process=True)