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

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_status_code(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.headers.get("Custom-Header") is None  # No custom header should be returned

def test_get_method_empty_response(app):
    @app.get("/empty")
    def empty_method(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""
    assert response.content_type == "text/plain; charset=utf-8"