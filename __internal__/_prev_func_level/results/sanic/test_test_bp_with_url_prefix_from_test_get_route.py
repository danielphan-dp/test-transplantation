import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    @app.route("/")
    def get_method(request):
        return text("I am get method", headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.headers["X-Custom-Header"] == "value"