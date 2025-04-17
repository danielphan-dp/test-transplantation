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

def test_get_method(app, handler):
    app.add_route(handler.get, "/")
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app, handler):
    app.add_route(handler.get, "/")
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming no change in response for query params

def test_get_method_with_custom_header(app, handler):
    app.add_route(handler.get, "/")
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming no change in response for custom headers

def test_get_method_with_invalid_method(app, handler):
    app.add_route(handler.get, "/")
    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text