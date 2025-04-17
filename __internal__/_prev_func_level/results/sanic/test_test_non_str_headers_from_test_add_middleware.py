import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_non_str_headers(app):
    @app.get("/test-headers")
    async def handler(request):
        headers = {"answer": 42}
        return text("Hello", headers=headers)

    request, response = app.test_client.get("/test-headers")
    assert response.headers.get("answer") == "42"

def test_get_method_with_query_params(app):
    @app.get("/test-query")
    async def handler(request):
        name = request.args.get("name", "World")
        return text(f"Hello, {name}")

    request, response = app.test_client.get("/test-query?name=Test")
    assert response.text == "Hello, Test"
    assert response.status == 200

def test_get_method_with_empty_query_params(app):
    @app.get("/test-empty-query")
    async def handler(request):
        name = request.args.get("name", "World")
        return text(f"Hello, {name}")

    request, response = app.test_client.get("/test-empty-query")
    assert response.text == "Hello, World"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text