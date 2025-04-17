import os
import logging
import pytest
from sanic import Sanic
from sanic import stop

SOCKPATH = "/tmp/sanic.sock"

@pytest.mark.xfail(reason='Flaky Test on Non Linux Infra')
def test_app_stop_removes_socket(caplog):
    app = Sanic(name="test")

    @app.after_server_start
    def running(app: Sanic):
        assert os.path.exists(SOCKPATH)
        stop(app)

    with pytest.raises(SystemExit):
        app.run(unix=SOCKPATH, single_process=True)

    assert not os.path.exists(SOCKPATH)

@pytest.mark.xfail(reason='Flaky Test on Non Linux Infra')
def test_app_stop_logs_info(caplog):
    app = Sanic(name="test")

    @app.after_server_start
    def running(app: Sanic):
        stop(app)

    with caplog.at_level(logging.INFO):
        app.run(unix=SOCKPATH, single_process=True)

    assert (
        "sanic.root",
        logging.INFO,
        f"Goin' Fast @ {SOCKPATH} http://...",
    ) in caplog.record_tuples

@pytest.mark.xfail(reason='Flaky Test on Non Linux Infra')
def test_app_stop_when_socket_not_created(caplog):
    app = Sanic(name="test")

    @app.after_server_start
    def running(app: Sanic):
        stop(app)

    if os.path.exists(SOCKPATH):
        os.remove(SOCKPATH)

    with caplog.at_level(logging.INFO):
        app.run(unix=SOCKPATH, single_process=True)

    assert not os.path.exists(SOCKPATH)