import logging
import pytest
from sanic import Sanic
from sanic_testing.testing import HOST, PORT, SanicTestClient

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop_functionality(app: Sanic, caplog):
    event = Event()

    @app.main_process_start
    async def main_start(app: Sanic):
        app.shared_ctx.event = event

    @app.after_server_start
    async def shutdown(app):
        app.stop()

    assert not event.is_set()
    app.stop()
    assert event.is_set()

    with caplog.at_level(logging.INFO):
        app.run()
    assert (
        "sanic.root",
        logging.INFO,
        "Application has been stopped.",
    ) in caplog.record_tuples

def test_app_stop_without_running(app: Sanic):
    with pytest.raises(RuntimeError):
        app.stop()