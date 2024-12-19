import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.get("/test")
def test_get_method(request):
    return text('I am get method')

def test_get_method_success(app):
    _, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.content_type == 'text/plain; charset=utf-8'

def test_get_method_not_found(app):
    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_error_handling(app):
    @app.get("/error")
    def error_response(request):
        raise Exception("Test Exception")
    
    _, response = app.test_client.get("/error")
    assert response.status == 500
    assert "Test Exception" in response.text