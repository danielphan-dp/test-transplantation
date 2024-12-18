import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test-get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/test-get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_custom_header(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/test-get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert request.headers.get("Custom-Header") == "value"

def test_get_method_invalid_route(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_server_port(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/test-get", headers={"Host": "my-server"})
    assert request.server_port == 80

def test_get_method_with_query_param(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/test-get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"