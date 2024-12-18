import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.testing import SanicTestClient

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

def test_get_method_invalid_route(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_header(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get", headers={"Custom-Header": "TestValue"})
    
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("Custom-Header") is None  # Custom headers should not affect response

def test_get_method_with_query_params(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get?param=value")
    
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure query params do not affect response

def test_get_method_multiple_requests(app):
    test_client = SanicTestClient(app)
    for _ in range(5):
        request, response = test_client.get("/get")
        assert response.status == 200
        assert response.text == 'I am get method'