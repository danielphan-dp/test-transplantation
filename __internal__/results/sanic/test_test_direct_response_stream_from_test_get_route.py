import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    class DummyView:
        def get(self, request: Request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")
    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
    assert "Content-Length" in response.headers

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers["X-Custom-Header"] == "value"  # Check if custom header is preserved

def test_get_method_empty_response(app):
    class EmptyView:
        def get(self, request: Request):
            return text("")

    app.add_route(EmptyView().get, "/empty")
    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""  # Check for empty response
    assert response.headers["Content-Length"] == "0"  # Ensure Content-Length is 0 for empty response