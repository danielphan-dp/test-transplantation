import logging
import os
import pytest
from sanic import Sanic

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_stop_method(app, caplog):
    app.after_server_start(lambda app, _: app.stop())

    with caplog.at_level(logging.INFO):
        app.prepare(fast=True)
        app.stop()

    assert app.state.fast
    assert app.state.workers == os.cpu_count() or 1

    messages = [m[2] for m in caplog.record_tuples]
    assert "Server stopped" in messages

def test_stop_without_start(app, caplog):
    with caplog.at_level(logging.INFO):
        app.stop()

    assert "Server stopped" in caplog.text

def test_stop_multiple_calls(app, caplog):
    app.after_server_start(lambda app, _: app.stop())

    with caplog.at_level(logging.INFO):
        app.prepare(fast=True)
        app.stop()
        app.stop()  # Call stop again

    assert app.state.fast
    assert "Server stopped" in caplog.text
    assert caplog.text.count("Server stopped") == 1  # Ensure it only logs once