import random
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_status_code(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_random_data(app):
    expected = random.choice(["Hello", "World", "Sanic", "Test"])
    @app.get(f"/get/{expected}")
    def dynamic_get(request, param):
        return text(f"I am get method with {param}")

    request, response = app.test_client.get(f"/get/{expected}")
    assert response.text == f"I am get method with {expected}"