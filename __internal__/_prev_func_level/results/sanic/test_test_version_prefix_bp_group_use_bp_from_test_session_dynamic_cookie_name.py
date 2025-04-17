import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    class DummyView:
        def get(self, request):
            return text('I am get method')
    return DummyView()

def test_get_method_response(app, handler):
    app.add_route(handler.get, "/get")
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app, handler):
    app.add_route(handler.get, "/get")
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app, handler):
    app.add_route(handler.get, "/get")
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the handler ignores query params

def test_get_method_with_different_path(app, handler):
    app.add_route(handler.get, "/different")
    request, response = app.test_client.get("/different")
    assert response.status == 200
    assert response.text == "I am get method"