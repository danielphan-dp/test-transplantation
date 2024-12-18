import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("test_app")
    return app

class DummyView:
    def get(self, request):
        return text('I am get method')

def test_get_method(json_app):
    json_app.add_route(DummyView().get, "/get")
    
    request, response = json_app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"
    assert "Content-Length" in response.headers
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

def test_get_method_with_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(json_app):
    json_app.add_route(DummyView().get, "/get-custom-header")
    
    request, response = json_app.test_client.get("/get-custom-header", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers["X-Custom-Header"] == "value"  # Check if custom header is passed through

def test_get_method_with_query_params(json_app):
    json_app.add_route(DummyView().get, "/get-query")
    
    request, response = json_app.test_client.get("/get-query?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Ensure query params do not affect response content

def test_get_method_with_empty_response(json_app):
    class EmptyResponseView:
        def get(self, request):
            return text("", status=204)

    json_app.add_route(EmptyResponseView().get, "/empty")
    
    request, response = json_app.test_client.get("/empty")
    assert response.status == 204
    assert response.text == ""
    assert "Content-Length" not in response.headers
    assert "Content-Type" not in response.headers