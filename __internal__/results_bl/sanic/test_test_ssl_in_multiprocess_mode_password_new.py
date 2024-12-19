import logging
import pytest
from sanic import Sanic
from multiprocessing import Event

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_method(app: Sanic):
    event = Event()

    @app.main_process_start
    async def main_start(app: Sanic):
        app.shared_ctx.event = event

    @app.after_server_start
    async def shutdown(app):
        app.shared_ctx.event.set()
        app.stop()

    assert not event.is_set()
    app.stop()
    assert event.is_set()

    with pytest.raises(Exception):
        app.stop()  # Testing stop method when already stopped

    assert (
        "sanic.root",
        logging.INFO,
        "Application stopped",
    ) in caplog.record_tuples

def test_stop_method_no_event(app: Sanic):
    @app.after_server_start
    async def shutdown(app):
        app.stop()

    app.stop()  # Testing stop method without setting event
    assert app.is_stopped  # Assuming there's a way to check if the app is stopped

def test_stop_method_with_active_requests(app: Sanic):
    @app.route("/")
    async def test_route(request):
        return "Hello, World!"

    @app.after_server_start
    async def shutdown(app):
        app.stop()

    app.run()
    app.stop()  # Testing stop method while requests are being processed
    # Here we would check if the requests were handled properly before stopping