import pytest
from sanic import Sanic
from multiprocessing import Event
from sanic.worker.multiplexer import WorkerMultiplexer

def test_stop_app_without_multiplexer():
    event = Event()
    app = Sanic("TestApp")

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event

    app.run(single_process=True)

    assert not event.is_set()

    app.stop()
    assert app.is_stopped

def test_stop_app_with_multiplexer():
    event = Event()
    app = Sanic("TestAppWithMultiplexer")
    app.m = WorkerMultiplexer()

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event

    @app.after_server_start
    def stop(app):
        if hasattr(app, "m") and isinstance(app.m, WorkerMultiplexer):
            app.shared_ctx.event.set()
        app.stop()

    app.run(single_process=True)

    assert event.is_set()  # Ensure the event is set when multiplexer is present
    assert app.is_stopped

def test_stop_app_multiple_times():
    app = Sanic("TestAppMultipleStops")
    app.m = WorkerMultiplexer()

    app.stop()  # First stop
    assert app.is_stopped

    app.stop()  # Second stop
    assert app.is_stopped  # Ensure it remains stopped after multiple calls

def test_stop_app_no_multiplexer_event_not_set():
    event = Event()
    app = Sanic("TestAppNoMultiplexer")

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event

    app.run(single_process=True)

    app.stop()
    assert not event.is_set()  # Ensure event is not set when no multiplexer is present