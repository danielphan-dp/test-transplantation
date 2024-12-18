import json
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("test_app")

    @app.get("/test-get")
    async def handler_get(request: Request):
        return text("I am get method")

    return app

def test_get_method(json_app):
    request, response = json_app.test_client.get("/test-get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid-route")
    assert response.status == 404

def test_get_method_with_query_params(json_app):
    request, response = json_app.test_client.get("/test-get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_headers(json_app):
    headers = {"Custom-Header": "value"}
    request, response = json_app.test_client.get("/test-get", headers=headers)
    assert response.status == 200
    assert response.text == "I am get method"