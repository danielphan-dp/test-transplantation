import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_success(app):
    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.content_type == 'text/plain; charset=utf-8'

def test_get_method_not_found(app):
    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_empty_request(app):
    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/get", headers={'Content-Length': '0'})
    assert response.status == 200
    assert response.text == 'I am get method'