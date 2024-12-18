import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

    request, response = app.test_client.get("/get/")
    assert response.status == 404

def test_get_method_with_invalid_route():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_query_params():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"