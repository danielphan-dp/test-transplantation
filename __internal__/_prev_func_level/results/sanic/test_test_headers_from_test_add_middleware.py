import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_headers(app):
    @app.get("/get_with_headers")
    async def get_with_headers(request):
        return text("I am get method", headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/get_with_headers")
    assert response.headers.get("X-Custom-Header") == "value"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_with_query")
    async def get_with_query(request):
        name = request.args.get("name", "Guest")
        return text(f"I am get method, {name}")

    request, response = app.test_client.get("/get_with_query?name=John")
    assert response.text == "I am get method, John"