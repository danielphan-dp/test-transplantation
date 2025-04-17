import asyncio
import logging
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_exception(app, monkeypatch, caplog):
    def mock_error_handler_response(*args, **kwargs):
        raise SanicException("Mock SanicException")

    monkeypatch.setattr(app.error_handler, "response", mock_error_handler_response)

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.get("/")
    
    assert response.status == 500
    assert "Mock SanicException" in response.text
    assert "Exception occurred while handling uri: 'http://127.0.0.1:" in caplog.text

def test_get_method_with_empty_response(app):
    @app.get("/empty")
    def empty_handler(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""