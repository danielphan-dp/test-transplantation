import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_empty_path(app):
    request, response = app.test_client.get("")
    assert response.status == 404

def test_get_method_with_special_characters(app):
    request, response = app.test_client.get("/folder/test@123/end/")
    assert response.status == 404

def test_get_method_with_multiple_slashes(app):
    request, response = app.test_client.get("/folder/test/////end/")
    assert response.status == 404