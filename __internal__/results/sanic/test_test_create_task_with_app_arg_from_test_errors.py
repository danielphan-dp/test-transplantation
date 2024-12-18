import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_param(app):
    @app.route("/get")
    async def get_method(request):
        name = request.args.get('name', 'World')
        return text(f"I am get method with {name}")

    request, response = app.test_client.get("/get?name=Test")
    assert response.text == "I am get method with Test"
    assert response.status == 200

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_method_not_allowed(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

def test_get_method_with_empty_response(app):
    @app.route("/empty")
    async def empty_method(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""
    assert response.status == 200