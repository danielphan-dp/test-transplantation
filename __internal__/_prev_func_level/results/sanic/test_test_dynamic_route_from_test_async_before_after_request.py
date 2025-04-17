import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method"  # Ensure query params do not affect response

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"  # Ensure headers do not affect response

def test_get_method_empty_response(app):
    @app.get("/empty")
    def empty_method(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""  # Test for empty response handling

def test_get_method_invalid_method(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text