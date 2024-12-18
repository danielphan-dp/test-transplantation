import asyncio
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/")
    async def get_method(request: Request):
        return text("I am get method")

    return app

def test_get_method_status(app):
    request, response = app.test_client.get("/")
    assert response.status == 200

def test_get_method_response_text(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_without_cookies(app):
    request, response = app.test_client.get("/")
    assert response.cookies == {}

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # No custom header in response