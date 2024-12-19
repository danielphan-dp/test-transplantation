import logging
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("test_stop_app")
    return app

def test_stop_app_success(app):
    @app.after_server_start
    def after_start(*args):
        app.stop()

    with pytest.raises(SanicException):
        app.run(host="127.0.0.1", port=42102, single_process=True)

def test_stop_app_no_running_server(app):
    with pytest.raises(SanicException):
        app.stop()

def test_stop_app_logging(caplog, app):
    @app.after_server_start
    def after_start(*args):
        app.stop()

    with caplog.at_level(logging.INFO):
        app.run(host="127.0.0.1", port=42102, single_process=True)

    assert "Server stopped" in caplog.text

def test_stop_app_multiple_stops(app):
    @app.after_server_start
    def after_start(*args):
        app.stop()
        app.stop()  # Attempt to stop again

    with pytest.raises(SanicException):
        app.run(host="127.0.0.1", port=42102, single_process=True)