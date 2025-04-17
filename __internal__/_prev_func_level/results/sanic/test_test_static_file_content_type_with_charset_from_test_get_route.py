import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

class DummyView:
    def get(self, request):
        return text("I am get method")

def test_get_method_response(app):
    app.add_route(DummyView().get, "/get")
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    app.add_route(DummyView().get, "/get_with_header")
    request, response = app.test_client.get("/get_with_header", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers.get("Custom-Header") is None  # No custom header in response

def test_get_method_with_query_param(app):
    app.add_route(DummyView().get, "/get_with_query")
    request, response = app.test_client.get("/get_with_query?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # No change in response for query param

def test_get_method_empty_response(app):
    class EmptyView:
        def get(self, request):
            return text("")
    
    app.add_route(EmptyView().get, "/empty")
    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""  # Check for empty response

def test_get_method_with_charset(app):
    app.add_route(DummyView().get, "/get_with_charset")
    request, response = app.test_client.get("/get_with_charset")
    assert response.status == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"  # Default charset check