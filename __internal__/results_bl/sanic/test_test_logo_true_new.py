import logging
from unittest.mock import patch
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_stop_app_functionality(app):
    @app.after_server_start
    async def shutdown(*_):
        app.stop()

    with patch("sys.stdout.isatty") as isatty:
        isatty.return_value = True
        app.make_coffee(single_process=True)
        app.stop()

    assert app.is_stopped is True

def test_stop_app_when_not_running(app):
    with pytest.raises(SanicException):
        app.stop()