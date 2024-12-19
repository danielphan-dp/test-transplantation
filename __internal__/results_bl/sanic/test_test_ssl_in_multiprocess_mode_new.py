import logging
import pytest
from sanic import Sanic
from sanic_testing.testing import HOST, PORT, SanicTestClient

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_method(app: Sanic):
    event = Event()
    
    @app.main_process_start
    async def main_start(app: Sanic):
        app.shared_ctx.event = event

    assert not event.is_set()
    app.stop()
    assert event.is_set()  # Ensure that stop method sets the event

def test_stop_method_no_event(app: Sanic):
    app.stop()  # Test stop method when no event is set
    # No assertion needed, just ensuring no exceptions are raised

def test_stop_method_multiple_calls(app: Sanic):
    event = Event()
    
    @app.main_process_start
    async def main_start(app: Sanic):
        app.shared_ctx.event = event

    app.stop()  # First call
    app.stop()  # Second call, should not raise an error
    assert event.is_set()  # Ensure that event is still set after multiple calls

def test_stop_method_with_logging(app: Sanic, caplog):
    with caplog.at_level(logging.INFO):
        app.stop()
    assert ("sanic.root", logging.INFO, "Application stopped") in caplog.record_tuples  # Assuming this log is generated on stop