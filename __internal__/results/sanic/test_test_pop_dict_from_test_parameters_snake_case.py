import json
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test-get")
    async def handler_get(request: Request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/test-get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test-get-with-params")
    async def handler_get_with_params(request: Request):
        name = request.args.get("name", "Guest")
        return text(f"I am get method, {name}")

    request, response = app.test_client.get("/test-get-with-params?name=John")
    assert response.status == 200
    assert response.text == "I am get method, John"

def test_get_method_with_no_query_params(app):
    request, response = app.test_client.get("/test-get-with-params")
    assert response.status == 200
    assert response.text == "I am get method, Guest"