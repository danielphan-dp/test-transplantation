import os
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

SOCKPATH = "/tmp/sanic.sock"

def test_app_stop():
    app = Sanic(name="test_app")

    @app.after_server_start
    async def after_start(app: Sanic):
        app.stop()

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)

    assert not app.is_running

def test_app_stop_with_exception():
    app = Sanic(name="test_app_exception")

    @app.after_server_start
    async def after_start(app: Sanic):
        raise SanicException("Forced exception to test stop behavior")

    with pytest.raises(SanicException, match="Forced exception to test stop behavior"):
        app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)

    assert not app.is_running

def test_app_stop_multiple_stops():
    app = Sanic(name="test_app_multiple")

    @app.after_server_start
    async def after_start(app: Sanic):
        app.stop()
        app.stop()  # Calling stop again to test idempotency

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)

    assert not app.is_running

def test_app_stop_with_cleanup():
    app = Sanic(name="test_app_cleanup")

    @app.after_server_start
    async def after_start(app: Sanic):
        os.unlink(SOCKPATH)
        app.stop()

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)

    assert not app.is_running
    assert not os.path.exists(SOCKPATH)