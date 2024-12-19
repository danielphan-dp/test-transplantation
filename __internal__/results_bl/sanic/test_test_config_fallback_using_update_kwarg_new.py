import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_returns_correct_response(app):
    @app.get("/test")
    def test_get(request):
        return text('I am get method')

    _, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    @app.get("/test")
    def test_get(request):
        return text('I am get method')

    _, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert response.content_type == "text/plain; charset=utf-8"