import logging
import os
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_stop_method(app, caplog):
    @app.after_server_start
    async def after_start(app, _):
        app.stop()

    with caplog.at_level(logging.INFO):
        app.prepare(fast=True)
        app.stop()

    assert app.state.fast is False
    assert app.state.workers == 0

    messages = [m[2] for m in caplog.record_tuples]
    assert "Application has been stopped." in messages

def test_stop_method_with_exception(app, caplog):
    @app.after_server_start
    async def after_start(app, _):
        raise RuntimeError("Forced exception during stop")

    with caplog.at_level(logging.ERROR):
        with pytest.raises(RuntimeError, match="Forced exception during stop"):
            app.stop()

    error_messages = [record.message for record in caplog.records if record.levelname == "ERROR"]
    assert "Forced exception during stop" in error_messages.pop(0)