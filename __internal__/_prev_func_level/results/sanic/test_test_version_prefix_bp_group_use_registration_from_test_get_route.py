import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    class DummyView:
        def get(self, request):
            return text("I am get method")
    return DummyView()

def test_get_method_response(app, handler):
    app.add_route(handler.get, "/get")
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app, handler):
    app.add_route(handler.get, "/get_with_param")
    request, response = app.test_client.get("/get_with_param?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Adjust based on expected behavior with params

def test_get_method_with_invalid_method(app, handler):
    app.add_route(handler.get, "/get")
    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text