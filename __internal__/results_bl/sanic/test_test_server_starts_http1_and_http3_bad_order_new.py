import logging
import sys
import pytest
from sanic import Sanic
from sanic.compat import UVLOOP_INSTALLED

@pytest.mark.skipif(sys.version_info < (3, 8) and (not UVLOOP_INSTALLED), reason='In 3.7 w/o uvloop the port is not always released')
def test_stop_method_stops_app(app: Sanic):
    app.stop()
    assert app.is_stopped is True

def test_stop_method_called_twice_does_not_raise(app: Sanic):
    app.stop()
    app.stop()  # Calling stop again should not raise an error
    assert app.is_stopped is True

def test_stop_method_with_active_requests(app: Sanic):
    @app.route('/')
    async def test_route(request):
        return 'Hello, World!'

    app.stop()  # Stop the app while there are active requests
    assert app.is_stopped is True

def test_stop_method_logs_stopping(app: Sanic, caplog):
    with caplog.at_level(logging.INFO):
        app.stop()
    assert "Stopping Sanic application" in caplog.text

def test_stop_method_does_not_affect_new_requests(app: Sanic):
    app.stop()
    response = app.test_client.get('/')
    assert response.status == 404  # Assuming the app is stopped, it should return 404