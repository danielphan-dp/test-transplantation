import asyncio
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
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_different_hosts(app):
    test_client = SanicTestClient(app, port=42101)
    site1 = f"127.0.0.1:{test_client.port}"
    request, response = test_client.get(f"http://{site1}/get")
    assert response.status == 200
    assert response.text == "I am get method"