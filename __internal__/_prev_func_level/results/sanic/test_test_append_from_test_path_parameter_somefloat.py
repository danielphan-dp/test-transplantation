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

def test_get_method_with_query_param(json_app):
    @json_app.get("/get-method")
    async def handler_get(request: Request):
        return text(f"I am get method with query param: {request.args.get('param')}")

    request, response = json_app.test_client.get("/get-method?param=test")
    assert response.text == "I am get method with query param: test"

def test_get_method_with_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_empty_response(json_app):
    @json_app.get("/empty-response")
    async def handler_empty(request: Request):
        return text("")

    request, response = json_app.test_client.get("/empty-response")
    assert response.text == ""