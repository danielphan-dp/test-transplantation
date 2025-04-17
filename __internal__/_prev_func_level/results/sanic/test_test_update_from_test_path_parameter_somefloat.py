import json
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("test_app")
    return app

def test_get_method(json_app):
    @json_app.get("/get-method")
    async def handler_get(request: Request):
        return text("I am get method")

    request, response = json_app.test_client.get("/get-method")
    assert response.text == "I am get method"

def test_get_method_with_empty_request(json_app):
    @json_app.get("/get-method-empty")
    async def handler_get_empty(request: Request):
        return text("I am get method")

    request, response = json_app.test_client.get("/get-method-empty")
    assert response.text == "I am get method"

def test_get_method_with_query_param(json_app):
    @json_app.get("/get-method-query")
    async def handler_get_query(request: Request):
        return text(f"I am get method with query param: {request.args.get('param')}")

    request, response = json_app.test_client.get("/get-method-query?param=test")
    assert response.text == "I am get method with query param: test"