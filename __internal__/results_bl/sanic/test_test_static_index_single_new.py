import os
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.body == b'I am get method'
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

def test_get_method_invalid_route(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_empty_request(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/test", headers={})
    assert response.status == 200
    assert response.body == b'I am get method'