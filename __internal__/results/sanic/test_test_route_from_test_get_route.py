import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

class DummyView:
    def get(self, request):
        return text("I am get method")

def test_get_method_response(app):
    app.add_route(DummyView().get, "/")
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    app.add_route(DummyView().get, "/")
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the handler does not change based on query params

def test_get_method_with_custom_header(app):
    app.add_route(DummyView().get, "/")
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the handler does not change based on headers

def test_get_method_invalid_method(app):
    app.add_route(DummyView().get, "/")
    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text