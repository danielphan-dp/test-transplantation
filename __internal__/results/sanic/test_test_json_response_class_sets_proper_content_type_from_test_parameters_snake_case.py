import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get-method")
    async def handler(request: Request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get-method")
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get-method-with-params")
    async def handler(request: Request):
        name = request.args.get("name", "World")
        return text(f"I am get method, {name}")

    request, response = app.test_client.get("/get-method-with-params?name=Test")
    assert response.text == "I am get method, Test"
    assert response.status == 200

def test_get_method_without_query_params(app):
    request, response = app.test_client.get("/get-method-with-params")
    assert response.text == "I am get method, World"
    assert response.status == 200