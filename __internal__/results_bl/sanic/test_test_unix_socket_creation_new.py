import logging
import os
import pytest
from sanic import Sanic
from socket import AF_UNIX, socket

SOCKPATH = "/tmp/test.sock"

@pytest.mark.xfail(reason='Flaky Test on Non Linux Infra')
def test_app_stop_functionality(caplog):
    app = Sanic(name="test")

    @app.after_server_start
    def running(app: Sanic):
        app.stop()

    with caplog.at_level(logging.INFO):
        app.run(unix=SOCKPATH, single_process=True)

    assert (
        "sanic.root",
        logging.INFO,
        f"Goin' Fast @ {SOCKPATH} http://...",
    ) in caplog.record_tuples
    assert not os.path.exists(SOCKPATH)

def test_app_stop_without_running(caplog):
    app = Sanic(name="test")
    app.stop()
    assert not app.is_running

def test_app_stop_multiple_calls(caplog):
    app = Sanic(name="test")

    @app.after_server_start
    def running(app: Sanic):
        app.stop()
        app.stop()  # Calling stop again

    with caplog.at_level(logging.INFO):
        app.run(unix=SOCKPATH, single_process=True)

    assert not os.path.exists(SOCKPATH)