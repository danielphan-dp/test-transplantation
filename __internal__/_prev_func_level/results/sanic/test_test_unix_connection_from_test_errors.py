import os
import pytest
from sanic import Sanic
from sanic.request import Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic(name="test")
    return app

def test_get_method(app):
    @app.get("/")
    def handler(request: Request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_unexpected_method(app):
    @app.get("/")
    def handler(request: Request):
        return text('I am get method')

    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/")
    def handler(request: Request):
        return text('I am get method', headers={'X-Custom-Header': 'Test'})

    request, response = app.test_client.get("/")
    assert response.headers.get('X-Custom-Header') == 'Test'