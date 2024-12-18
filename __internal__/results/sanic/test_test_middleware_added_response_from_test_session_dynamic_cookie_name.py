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

def test_get_method_status_code(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/get_with_header")
    def get_with_header(request):
        return text("I am get method with header", headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/get_with_header")
    assert response.headers["X-Custom-Header"] == "value"