import asyncio
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request: Request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_context(app):
    @app.route("/", ctx_foo="foo", ctx_bar=99)
    async def handler_with_context(request: Request):
        return text("I am get method with context")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert request.route.ctx.foo == "foo"
    assert request.route.ctx.bar == 99

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_context(app):
    class CustomContext:
        pass

    @app.get("/", ctx=CustomContext())
    async def handler_with_custom_context(request: Request):
        return text("I am get method with custom context")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method with custom context"