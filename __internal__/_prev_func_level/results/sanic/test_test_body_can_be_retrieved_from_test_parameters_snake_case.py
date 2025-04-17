import json
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    async def get_with_params(request):
        name = request.args.get("name", "default")
        return text(f"I am get method with name: {name}")

    request, response = app.test_client.get("/get_with_params?name=test")
    assert response.text == "I am get method with name: test"
    assert response.status == 200

def test_get_method_with_no_query_params(app):
    @app.get("/get_with_no_params")
    async def get_with_no_params(request):
        return text("I am get method with no params")

    request, response = app.test_client.get("/get_with_no_params")
    assert response.text == "I am get method with no params"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_headers(app):
    @app.get("/get_with_headers")
    async def get_with_headers(request):
        return text("I am get method with headers")

    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/get_with_headers", headers=headers)
    assert response.text == "I am get method with headers"
    assert response.status == 200