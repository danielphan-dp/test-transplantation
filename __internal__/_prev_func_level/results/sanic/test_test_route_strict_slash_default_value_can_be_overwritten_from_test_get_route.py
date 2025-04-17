import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_get_method")
    return app

def test_get_method(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_strict_slash(app):
    @app.get("/get/", strict_slashes=False)
    def handler(request):
        return text("I am get method with strict slash")

    request, response = app.test_client.get("/get/")
    assert response.status == 200
    assert response.text == "I am get method with strict slash"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_invalid_method(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text