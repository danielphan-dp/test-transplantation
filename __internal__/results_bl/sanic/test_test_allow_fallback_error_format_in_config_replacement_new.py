import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_returns_text(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.body == b'I am get method'

def test_get_method_with_invalid_route(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_empty_response(app):
    @app.get("/empty")
    def get_method(request):
        return text('')

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.body == b''

def test_get_method_with_special_characters(app):
    @app.get("/special")
    def get_method(request):
        return text('I am get method with special characters: !@#$%^&*()')

    request, response = app.test_client.get("/special")
    assert response.status == 200
    assert response.body == b'I am get method with special characters: !@#$%^&*()'