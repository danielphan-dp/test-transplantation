import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/non_existent_route")
    
    assert response.status == 404
    assert "File not found" in response.text

def test_get_method_empty_request(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test", headers={})
    
    assert response.status == 200
    assert response.text == 'I am get method'