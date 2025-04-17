import asyncio
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def get_method(request: Request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_status_code(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200

def test_get_method_with_custom_header(app):
    @app.route("/get_with_header")
    async def get_with_header(request: Request):
        return text('I am get method with header', headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/get_with_header")
    assert response.headers["X-Custom-Header"] == "value"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_param(app):
    @app.route("/get_with_param")
    async def get_with_param(request: Request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Received param: test"