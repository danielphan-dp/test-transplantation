import json
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    async def test_get_method(request: Request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/custom-header")
    async def custom_header(request: Request):
        return text("I am get method", headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/custom-header")
    assert response.headers["X-Custom-Header"] == "value"

def test_get_method_with_query_param(app):
    @app.get("/query")
    async def query_param(request: Request):
        name = request.args.get("name", "World")
        return text(f"I am get method, {name}")

    request, response = app.test_client.get("/query?name=Tester")
    assert response.text == "I am get method, Tester"