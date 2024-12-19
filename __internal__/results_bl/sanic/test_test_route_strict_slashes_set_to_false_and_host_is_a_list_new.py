import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_delete_method_with_valid_request(app):
    @app.delete("/delete", strict_slashes=False)
    def delete_handler(request):
        return text("I am delete method")

    test_client = SanicTestClient(app)
    request, response = test_client.delete("/delete")
    assert response.text == "I am delete method"

def test_delete_method_with_invalid_route(app):
    test_client = SanicTestClient(app)
    request, response = test_client.delete("/nonexistent")
    assert response.status == 404

def test_delete_method_with_empty_request(app):
    @app.delete("/delete", strict_slashes=False)
    def delete_handler(request):
        return text("I am delete method")

    test_client = SanicTestClient(app)
    request, response = test_client.delete("/delete", json={})
    assert response.text == "I am delete method"

def test_delete_method_with_different_host(app):
    site1 = "127.0.0.1:42101"
    @app.delete("/delete", host=[site1], strict_slashes=False)
    def delete_handler(request):
        return text("I am delete method")

    test_client = SanicTestClient(app, port=42101)
    request, response = test_client.delete(f"http://{site1}/delete")
    assert response.text == "I am delete method"