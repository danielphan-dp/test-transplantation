import asyncio
import logging
from typing import Callable, List
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import ServerError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/")
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_exception(app, caplog: LogCaptureFixture):
    exception_handler_ran = False

    @app.exception(ServerError)
    async def exception_handler(request, exception):
        nonlocal exception_handler_ran
        exception_handler_ran = True
        return text("Error")

    @app.route("/error")
    async def error_route(request):
        raise ServerError("Exception")

    with caplog.at_level(logging.WARNING):
        request, response = app.test_client.get("/error")
        assert "Error" in response.text
        assert exception_handler_ran is True

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_logging(app, caplog: LogCaptureFixture):
    @app.route("/log")
    async def log_route(request):
        return text("Logging test")

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/log")
        assert response.text == "Logging test"
        assert "Logging test" in caplog.text