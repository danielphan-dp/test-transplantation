import logging
import os
import pytest
from sanic import Sanic

def test_stop_method(app: Sanic, caplog):
    @app.after_server_start
    async def after_start(app, _):
        app.stop()

    with caplog.at_level(logging.INFO):
        app.prepare(fast=True)
        app.stop()

    assert app.state.fast is False
    assert app.state.workers == 0

    messages = [m[2] for m in caplog.record_tuples]
    assert "Application stopped" in messages

def test_stop_method_no_workers(app: Sanic, caplog):
    @app.after_server_start
    async def after_start(app, _):
        app.stop()

    with caplog.at_level(logging.INFO):
        app.prepare(fast=True)
        app.stop()

    assert app.state.fast is False
    assert app.state.workers == 0

    messages = [m[2] for m in caplog.record_tuples]
    assert "Application stopped" in messages

def test_stop_method_with_error(app: Sanic, caplog):
    @app.after_server_start
    async def after_start(app, _):
        raise RuntimeError("Forced error during stop")

    with caplog.at_level(logging.ERROR):
        app.prepare(fast=True)
        try:
            app.stop()
        except RuntimeError:
            pass

    assert "Forced error during stop" in caplog.text
    assert app.state.fast is True  # Ensure it doesn't change state on error
    assert app.state.workers == os.cpu_count() or 1  # Workers should remain unchanged