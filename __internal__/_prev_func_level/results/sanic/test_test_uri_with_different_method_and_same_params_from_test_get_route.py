import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/", methods=["GET"])
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_different_params(app):
    @app.route("/<param>", methods=["GET"])
    async def get_with_param(request, param):
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test_param")
    assert response.status == 200
    assert response.text == "Received param: test_param"