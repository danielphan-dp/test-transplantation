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
        name = request.args.get("name", "World")
        return text(f"I am get method, {name}")

    request, response = json_app.test_client.get("/get-method?name=Tester")
    assert response.text == "I am get method, Tester"

def test_get_method_with_empty_query_param(json_app):
    @json_app.get("/get-method")
    async def handler_get(request: Request):
        name = request.args.get("name", "World")
        return text(f"I am get method, {name}")

    request, response = json_app.test_client.get("/get-method?name=")
    assert response.text == "I am get method, "