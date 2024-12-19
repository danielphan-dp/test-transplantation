import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_delete_method(app):
    @app.delete("/delete", strict_slashes=False)
    def delete_handler(request):
        return text("I am delete method")

    test_client = SanicTestClient(app)
    request, response = test_client.delete("/delete")
    assert response.text == "I am delete method"

def test_delete_method_not_found(app):
    test_client = SanicTestClient(app)
    request, response = test_client.delete("/nonexistent")
    assert response.status == 404

def test_delete_method_with_host(app):
    site1 = "127.0.0.1:8000"
    
    @app.delete("/delete", host=[site1], strict_slashes=False)
    def delete_handler(request):
        return text("I am delete method with host")

    test_client = SanicTestClient(app)
    request, response = test_client.delete(f"http://{site1}/delete")
    assert response.text == "I am delete method with host"

def test_delete_method_invalid_host(app):
    site1 = "127.0.0.1:8000"
    
    @app.delete("/delete", host=["invalid.com"], strict_slashes=False)
    def delete_handler(request):
        return text("This should not be reachable")

    test_client = SanicTestClient(app)
    request, response = test_client.delete(f"http://{site1}/delete")
    assert response.status == 404

def test_delete_method_strict_slashes(app):
    @app.delete("/delete/", strict_slashes=True)
    def delete_handler(request):
        return text("I am delete method with strict slashes")

    test_client = SanicTestClient(app)
    request, response = test_client.delete("/delete/")
    assert response.text == "I am delete method with strict slashes"

    request, response = test_client.delete("/delete")
    assert response.status == 404