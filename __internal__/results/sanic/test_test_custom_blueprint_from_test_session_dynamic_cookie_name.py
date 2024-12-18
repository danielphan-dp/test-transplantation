import pytest
from sanic import Sanic, Blueprint, text

def test_get_method():
    app = Sanic("test_app")

    @app.route("/")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route():
    app = Sanic("test_app")

    @app.route("/")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_header():
    app = Sanic("test_app")

    @app.route("/")
    def get_method(request):
        return text("I am get method", headers={"X-Custom-Header": "CustomValue"})

    request, response = app.test_client.get("/")
    
    assert response.headers["X-Custom-Header"] == "CustomValue"