import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/test")
    def test_get(request):
        return text("I am get method")
    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/test", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"