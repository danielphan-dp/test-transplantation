import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_with_valid_host(app):
    test_client = SanicTestClient(app)
    site1 = "127.0.0.1:8000"

    @app.get("/get", host=[site1], strict_slashes=False)
    def get_handler(request):
        return text("I am get method")

    request, response = test_client.get(f"http://{site1}/get")
    assert response.text == "I am get method"

def test_get_method_with_invalid_host(app):
    test_client = SanicTestClient(app)
    site1 = "127.0.0.1:8000"
    invalid_host = "invalid.site.com"

    @app.get("/get", host=[site1], strict_slashes=False)
    def get_handler(request):
        return text("I am get method")

    request, response = test_client.get(f"http://{invalid_host}/get")
    assert response.status == 404

def test_get_method_with_multiple_hosts(app):
    test_client = SanicTestClient(app)
    site1 = "127.0.0.1:8000"
    site2 = "example.com"

    @app.get("/get", host=[site1, site2], strict_slashes=False)
    def get_handler(request):
        return text("I am get method")

    request, response = test_client.get(f"http://{site1}/get")
    assert response.text == "I am get method"

    request, response = test_client.get(f"http://{site2}/get")
    assert response.text == "I am get method"

def test_get_method_with_strict_slashes(app):
    test_client = SanicTestClient(app)
    site1 = "127.0.0.1:8000"

    @app.get("/get/", host=[site1], strict_slashes=True)
    def get_handler(request):
        return text("I am get method with strict slashes")

    request, response = test_client.get(f"http://{site1}/get/")
    assert response.text == "I am get method with strict slashes"

    request, response = test_client.get(f"http://{site1}/get")
    assert response.status == 404

def test_get_method_with_different_http_methods(app):
    test_client = SanicTestClient(app)
    site1 = "127.0.0.1:8000"

    @app.get("/get", host=[site1], strict_slashes=False)
    def get_handler(request):
        return text("I am get method")

    @app.post("/get", host=[site1], strict_slashes=False)
    def post_handler(request):
        return text("I am post method")

    request, response = test_client.get(f"http://{site1}/get")
    assert response.text == "I am get method"

    request, response = test_client.post(f"http://{site1}/get")
    assert response.text == "I am post method"