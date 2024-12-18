import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_not_found(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_strict_slash(app):
    @app.get("/get/", strict_slashes=True)
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_without_strict_slash(app):
    @app.get("/get/", strict_slashes=True)
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 404

def test_get_method_with_invalid_method(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text