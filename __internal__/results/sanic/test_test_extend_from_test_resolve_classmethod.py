import json
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get-method")
    async def get_method_handler(request: Request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get-method")
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get-method-with-params")
    async def get_method_with_params_handler(request: Request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/get-method-with-params?param=test")
    assert response.text == "I am get method with param: test"

def test_get_method_without_query_params(app):
    request, response = app.test_client.get("/get-method-with-params")
    assert response.text == "I am get method with param: default"