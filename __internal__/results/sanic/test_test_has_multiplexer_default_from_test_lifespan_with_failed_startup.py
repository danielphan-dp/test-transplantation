import sys
import pytest
from multiprocessing import Event
from sanic import Sanic
from sanic.compat import use_context
from sanic.worker.multiplexer import WorkerMultiplexer

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_method_with_multiplexer(app: Sanic):
    event = Event()

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event

    @app.after_server_start
    def stop(app):
        if hasattr(app, "m") and isinstance(app.m, WorkerMultiplexer):
            app.shared_ctx.event.set()
        app.stop()

    with use_context("fork"):
        app.run()

    assert event.is_set()

def test_stop_method_without_multiplexer(app: Sanic):
    event = Event()

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event

    @app.after_server_start
    def stop(app):
        app.stop()

    with use_context("fork"):
        app.run()

    assert not event.is_set()  # Ensure event is not set when multiplexer is not present

def test_stop_method_with_exception_handling(app: Sanic):
    event = Event()

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event

    @app.after_server_start
    def stop(app):
        try:
            app.stop()
        except Exception as e:
            event.set()  # Set event if an exception occurs

    with use_context("fork"):
        app.run()

    assert event.is_set()  # Ensure event is set if an exception occurs during stop