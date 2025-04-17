import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_test/")
    def get_handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get_test/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route/")
    assert response.status == 404

def test_get_method_with_slash(app):
    request, response = app.test_client.get("/get_test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_additional_slash(app):
    request, response = app.test_client.get("/get_test//")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get_test/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"