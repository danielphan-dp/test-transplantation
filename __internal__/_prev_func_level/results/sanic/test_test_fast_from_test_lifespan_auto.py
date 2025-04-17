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

    try:
        workers = len(os.sched_getaffinity(0))
    except AttributeError:
        workers = os.cpu_count() or 1

    with caplog.at_level(logging.INFO):
        app.prepare(fast=True)
        app.stop()

    assert app.state.fast is False
    assert app.state.workers == 0

    messages = [m[2] for m in caplog.record_tuples]
    assert "Application stopped" in messages

def test_stop_method_with_tasks(app: Sanic, caplog):
    @app.after_server_start
    async def after_start(app, _):
        app.stop()

    app.shutdown_tasks = Mock()

    with caplog.at_level(logging.INFO):
        app.prepare(fast=True)
        app.stop()

    app.shutdown_tasks.assert_called_once_with(timeout=0)

    assert app.state.fast is False
    assert app.state.workers == 0

    messages = [m[2] for m in caplog.record_tuples]
    assert "Application stopped" in messages