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
    request, response = test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_custom_host(app):
    site1 = "127.0.0.1:8000"
    
    @app.get("/get", host=[site1])
    def get_handler(request):
        return text("I am get method with custom host")

    test_client = SanicTestClient(app)
    request, response = test_client.get(f"http://{site1}/get")
    assert response.text == "I am get method with custom host"

def test_get_method_with_strict_slashes(app):
    @app.get("/get/", strict_slashes=False)
    def get_handler(request):
        return text("I am get method with strict slashes")

    test_client = SanicTestClient(app)
    request, response = test_client.get("/get/")
    assert response.text == "I am get method with strict slashes"

def test_get_method_with_query_parameters(app):
    @app.get("/get")
    def get_handler(request):
        param = request.args.get('param', 'default')
        return text(f"Received param: {param}")

    test_client = SanicTestClient(app)
    request, response = test_client.get("/get?param=test")
    assert response.text == "Received param: test"