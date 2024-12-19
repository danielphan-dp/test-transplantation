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

    _, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert response.content_type == "text/plain; charset=utf-8"