import logging
import pytest
from sanic import Sanic
from sanic_testing.testing import HOST, PORT, SanicTestClient
from multiprocessing import Event

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop_event(app: Sanic, caplog: pytest.LogCaptureFixture):
    event = Event()

    @app.main_process_start
    async def main_start(app: Sanic):
        app.shared_ctx.event = event

    @app.after_server_start
    async def shutdown(app):
        app.stop()

    assert not event.is_set()
    with use_context("fork"):
        with caplog.at_level(logging.INFO):
            app.run()
    assert event.is_set()

    assert (
        "sanic.root",
        logging.INFO,
        "Server stopped successfully",
    ) in caplog.record_tuples

def test_app_stop_no_event(app: Sanic):
    app.stop()
    assert not app.is_running()  # Ensure the app is not running after stop

def test_app_stop_multiple_calls(app: Sanic):
    app.stop()
    app.stop()  # Call stop multiple times
    assert not app.is_running()  # Ensure the app is still not running

def test_app_stop_with_tasks(app: Sanic):
    async def task():
        await asyncio.sleep(1)

    app.add_task(task())
    app.stop()
    assert not app.is_running()  # Ensure the app is not running after stop
    assert len(app.tasks) == 0  # Ensure all tasks are cleared after stop