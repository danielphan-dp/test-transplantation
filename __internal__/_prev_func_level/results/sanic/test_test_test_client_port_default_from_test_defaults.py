import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.testing import SanicTestClient, PORT

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_port(app):
    test_client = SanicTestClient(app)
    assert test_client.port == PORT  # Can be None before request

    request, response = test_client.get("/get")
    assert test_client.port > 0

def test_get_method_invalid_route(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_headers(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get", headers={"X-Custom-Header": "value"})
    
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("X-Custom-Header") is None  # No custom header in response

def test_get_method_with_query_params(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get?param=value")
    
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure query params do not affect response