import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    test_client = SanicTestClient(app)
    request, response = test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_strict_slashes(app):
    @app.get("/get/", strict_slashes=False)
    def get_handler(request):
        return text("I am get method with strict slashes")

    test_client = SanicTestClient(app)
    request, response = test_client.get("/get/")
    assert response.text == "I am get method with strict slashes"

def test_get_method_with_host(app):
    site1 = "127.0.0.1:8000"
    
    @app.get("/get", host=[site1], strict_slashes=False)
    def get_handler(request):
        return text("I am get method with host")

    test_client = SanicTestClient(app, port=8000)
    request, response = test_client.get(f"http://{site1}/get")
    assert response.text == "I am get method with host"

def test_get_method_with_different_hosts(app):
    site1 = "127.0.0.1:8000"
    site2 = "example.com"

    @app.get("/get", host=[site1, site2], strict_slashes=False)
    def get_handler(request):
        return text("I am get method for multiple hosts")

    test_client = SanicTestClient(app, port=8000)
    request, response = test_client.get(f"http://{site1}/get")
    assert response.text == "I am get method for multiple hosts"

    request, response = test_client.get("http://example.com/get")
    assert response.text == "I am get method for multiple hosts"