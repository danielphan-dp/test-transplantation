import logging
from typing import Callable, List
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import ServerError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_exception(app, caplog: pytest.LogCaptureFixture):
    @app.route("/error")
    async def error_route(request):
        raise ServerError("This is a server error")

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.get("/error")
        assert response.status == 500
        assert "This is a server error" in response.text

    assert any("An error occurred while handling the request" in message for message in caplog.text)