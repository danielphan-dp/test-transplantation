import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_strict_slashes(app):
    test_client = SanicTestClient(app)
    @app.get("/get/", strict_slashes=False)
    def get_handler_strict(request):
        return text("I am get method with strict slashes")

    request, response = test_client.get("/get/")
    assert response.text == "I am get method with strict slashes"

def test_get_method_with_different_hosts(app):
    test_client = SanicTestClient(app, port=42101)
    site1 = f"127.0.0.1:{test_client.port}"

    @app.get("/get", host=[site1, "site2.com"], strict_slashes=False)
    def get_handler_host(request):
        return text("OK")

    request, response = test_client.get("http://" + site1 + "/get")
    assert response.text == "OK"

    request, response = test_client.get("http://site2.com/get")
    assert response.status == 404  # Assuming site2.com is not set up for testing

def test_get_method_with_query_parameters(app):
    test_client = SanicTestClient(app)

    @app.get("/get")
    def get_handler_with_query(request):
        param = request.args.get('param', 'default')
        return text(f"Received param: {param}")

    request, response = test_client.get("/get?param=test")
    assert response.text == "Received param: test"

    request, response = test_client.get("/get?param=")
    assert response.text == "Received param: "