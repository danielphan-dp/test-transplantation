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
    with use_context("fork"):
        with caplog.at_level(logging.INFO):
            app.run()
    assert event.is_set()

    assert (
        "sanic.root",
        logging.INFO,
        "Application has stopped.",
    ) in caplog.record_tuples

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop_without_start(app: Sanic, caplog):
    with caplog.at_level(logging.INFO):
        app.stop()
    assert "Application has stopped." in caplog.text

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop_multiple_calls(app: Sanic, caplog):
    event = Event()

    @app.main_process_start
    async def main_start(app: Sanic):
        app.shared_ctx.event = event

    @app.after_server_start
    async def shutdown(app):
        app.stop()
        app.stop()  # Calling stop again

    assert not event.is_set()
    with use_context("fork"):
        with caplog.at_level(logging.INFO):
            app.run()
    assert event.is_set()

    assert (
        "sanic.root",
        logging.INFO,
        "Application has stopped.",
    ) in caplog.record_tuples