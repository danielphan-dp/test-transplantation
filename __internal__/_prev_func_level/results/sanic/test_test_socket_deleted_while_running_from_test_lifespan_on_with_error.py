import os
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

SOCKPATH = "/tmp/test.sock"

def test_app_stop():
    app = Sanic(name="test_app")

    @app.after_server_start
    async def after_start(app: Sanic):
        app.stop()

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)

    assert not app.is_running

def test_app_stop_with_error():
    app = Sanic(name="test_app_with_error")

    @app.after_server_start
    async def after_start_with_error(app: Sanic):
        raise RuntimeError("Simulated error during stop")
    
    with pytest.raises(RuntimeError, match="Simulated error during stop"):
        app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)

def test_app_stop_multiple_calls():
    app = Sanic(name="test_app_multiple_calls")

    @app.after_server_start
    async def after_start_multiple_calls(app: Sanic):
        app.stop()
        app.stop()  # Calling stop again to test idempotency

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)

    assert not app.is_running

def test_app_stop_no_running_instance():
    app = Sanic(name="test_app_no_running_instance")

    with pytest.raises(SanicException, match="Cannot stop a non-running application"):
        app.stop()