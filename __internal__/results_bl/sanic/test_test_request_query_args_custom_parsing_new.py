import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_query_args(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get?param=value")
    
    assert response.status == 200
    assert request.get_query_args(keep_blank_values=True) == [('param', 'value')]
    assert request.query_args == [('param', 'value')]

def test_get_method_with_no_query_args(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert request.get_query_args(keep_blank_values=True) == []
    assert request.query_args == []

def test_get_method_with_empty_query_args(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get?param=")
    
    assert response.status == 200
    assert request.get_query_args(keep_blank_values=True) == [('param', '')]
    assert request.query_args == []