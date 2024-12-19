import logging
import pytest
from unittest.mock import patch
from sanic import Sanic
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_app_stop(app):
    @app.after_server_start
    async def after_start(*_):
        app.stop()

    with patch("sys.stdout.isatty") as isatty:
        isatty.return_value = True
        with pytest.raises(SanicException):
            app.stop()

    assert not app.is_running

def test_app_stop_when_not_running(app):
    with patch("sys.stdout.isatty") as isatty:
        isatty.return_value = True
        app.stop()
        assert not app.is_running

def test_app_stop_logs_message(app, caplog):
    @app.after_server_start
    async def after_start(*_):
        app.stop()

    with patch("sys.stdout.isatty") as isatty:
        isatty.return_value = True
        with caplog.at_level(logging.DEBUG):
            app.stop()

    assert "App stopped" in caplog.text

def test_app_stop_multiple_calls(app):
    @app.after_server_start
    async def after_start(*_):
        app.stop()
        app.stop()  # Calling stop again

    with patch("sys.stdout.isatty") as isatty:
        isatty.return_value = True
        app.stop()
        assert not app.is_running