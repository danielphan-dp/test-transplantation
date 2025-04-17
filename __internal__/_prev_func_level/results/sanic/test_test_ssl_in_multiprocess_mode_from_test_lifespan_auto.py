import logging
import pytest
from sanic import Sanic
from sanic_testing.testing import HOST, PORT, SanicTestClient

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop_event(app: Sanic, caplog):
    event = Event()

    @app.main_process_start
    async def main_start(app: Sanic):
        app.shared_ctx.event = event

    @app.after_server_start
    async def shutdown(app):
        app.stop()

    assert not event.is_set()
    app.run()
    assert event.is_set()

    with caplog.at_level(logging.INFO):
        app.stop()
    assert (
        "sanic.root",
        logging.INFO,
        "Application stopped",
    ) in caplog.record_tuples

def test_app_stop_no_event(app: Sanic):
    app.stop()
    assert app.is_stopped()  # Assuming there's a method to check if the app is stopped

def test_app_stop_multiple_calls(app: Sanic):
    app.stop()
    app.stop()  # Calling stop multiple times
    assert app.is_stopped()  # Ensure it remains stopped after multiple calls

def test_app_stop_with_tasks(app: Sanic):
    async def shutdown_task():
        await asyncio.sleep(1)

    app.shutdown_tasks.append(shutdown_task)
    app.stop()
    assert app.is_stopped()  # Ensure the app stops even with tasks present