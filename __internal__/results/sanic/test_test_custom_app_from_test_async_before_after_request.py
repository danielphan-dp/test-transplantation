import pytest
from sanic import Sanic, Blueprint, text

def test_get_method():
    app = Sanic("test_app")
    
    @app.get("/")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route():
    app = Sanic("test_app")
    
    @app.get("/")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header():
    app = Sanic("test_app")
    
    @app.get("/")
    def get_method(request):
        return text('I am get method', headers={'X-Custom-Header': 'value'})

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'value'