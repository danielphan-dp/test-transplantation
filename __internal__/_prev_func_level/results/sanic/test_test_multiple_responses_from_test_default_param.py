import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test_get")
    def test_get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_headers(app):
    @app.get("/test_get_with_headers")
    def test_get_with_headers(request):
        return text("I am get method with headers", headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/test_get_with_headers")
    assert response.status == 200
    assert response.text == "I am get method with headers"
    assert response.headers["X-Custom-Header"] == "value"

def test_get_method_with_query_params(app):
    @app.get("/test_get_with_query")
    def test_get_with_query(request):
        name = request.args.get("name", "World")
        return text(f"I am get method, {name}")

    request, response = app.test_client.get("/test_get_with_query?name=Tester")
    assert response.status == 200
    assert response.text == "I am get method, Tester"

def test_get_method_without_query_params(app):
    request, response = app.test_client.get("/test_get_with_query")
    assert response.status == 200
    assert response.text == "I am get method, World"