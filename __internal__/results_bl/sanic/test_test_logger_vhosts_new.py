import logging
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

def test_stop_method():
    app = Sanic(name="test_stop_method")

    @app.after_server_start
    def start_server(*args):
        pass

    @app.after_server_stop
    def stop_server(*args):
        app.stop()

    app.run(host="127.0.0.1", port=42103, single_process=True)

    assert not app.is_running

def test_stop_method_when_not_running():
    app = Sanic(name="test_stop_method_when_not_running")

    with pytest.raises(SanicException):
        app.stop()