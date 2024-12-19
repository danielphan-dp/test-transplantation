import sys
import pytest
from multiprocessing import Event
from sanic import Sanic
from sanic.compat import use_context
from sanic.worker.multiplexer import WorkerMultiplexer

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop_without_multiplexer():
    app = Sanic("TestApp")
    event = Event()

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event

    @app.after_server_start
    def stop(app):
        app.stop()

    with use_context("fork"):
        app.run()

    assert event.is_set() == False

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop_with_multiplexer():
    app = Sanic("TestAppWithMultiplexer")
    event = Event()

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event
        app.m = WorkerMultiplexer()

    @app.after_server_start
    def stop(app):
        if hasattr(app, "m") and isinstance(app.m, WorkerMultiplexer):
            app.shared_ctx.event.set()
        app.stop()

    with use_context("fork"):
        app.run()

    assert event.is_set() == True

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop_multiple_starts():
    app = Sanic("TestAppMultipleStarts")
    event = Event()

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event

    @app.after_server_start
    def stop(app):
        app.stop()

    with use_context("fork"):
        app.run()
        app.run()  # Running again to check if stop works multiple times

    assert event.is_set() == False

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop_with_error_handling():
    app = Sanic("TestAppWithErrorHandling")
    event = Event()

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event

    @app.after_server_start
    def stop(app):
        try:
            app.stop()
        except Exception as e:
            event.set()  # Set event if there's an error

    with use_context("fork"):
        app.run()

    assert event.is_set() == False  # Ensure event is not set on successful stop