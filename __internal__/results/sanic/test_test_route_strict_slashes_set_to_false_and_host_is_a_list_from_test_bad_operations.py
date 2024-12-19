import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.put("/put", host=["127.0.0.1:42101", "site2.com"], strict_slashes=False)
    def put_handler(request):
        return text("I am put method")

    return app

def test_put_method_success(app):
    test_client = SanicTestClient(app, port=42101)
    request, response = test_client.put("http://127.0.0.1:42101/put")
    assert response.text == "I am put method"

def test_put_method_invalid_host(app):
    test_client = SanicTestClient(app, port=42101)
    request, response = test_client.put("http://invalid_host/put")
    assert response.status_code == 404

def test_put_method_with_different_host(app):
    test_client = SanicTestClient(app, port=42101)
    request, response = test_client.put("http://site2.com/put")
    assert response.text == "I am put method"

def test_put_method_no_slash(app):
    test_client = SanicTestClient(app, port=42101)
    request, response = test_client.put("http://127.0.0.1:42101/put/")
    assert response.text == "I am put method"

def test_put_method_with_payload(app):
    test_client = SanicTestClient(app, port=42101)
    request, response = test_client.put("http://127.0.0.1:42101/put", data="payload")
    assert response.text == "I am put method"  # Assuming the handler does not change behavior with payload