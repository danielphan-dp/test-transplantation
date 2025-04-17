import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_strict_slash(app):
    @app.get("/get/", strict_slashes=False)
    def get_handler(request):
        return text("I am get method with strict slash")

    request, response = app.test_client.get("/get/")
    assert response.status == 200
    assert response.text == "I am get method with strict slash"

def test_get_method_with_query_param(app):
    @app.get("/get")
    def get_handler(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_without_query_param(app):
    @app.get("/get")
    def get_handler(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "Received param: default"