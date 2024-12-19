import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    @app.get("/greet")
    async def greet(request):
        name = request.args.get("name", "World")
        return text(f"Hello, {name}!")

    request, response = app.test_client.get("/greet?name=Alice")
    assert response.status == 200
    assert response.text == "Hello, Alice!"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_invalid_method(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text