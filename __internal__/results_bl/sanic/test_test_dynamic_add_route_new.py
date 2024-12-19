import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/test")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    
    assert response.status == 404

def test_get_method_with_query_param(app):
    @app.get("/test")
    async def get_method(request):
        name = request.args.get('name', 'Guest')
        return text(f'Hello, {name}')

    request, response = app.test_client.get("/test?name=John")
    
    assert response.text == 'Hello, John'

def test_get_method_empty_query_param(app):
    @app.get("/test")
    async def get_method(request):
        name = request.args.get('name', 'Guest')
        return text(f'Hello, {name}')

    request, response = app.test_client.get("/test?name=")
    
    assert response.text == 'Hello, '