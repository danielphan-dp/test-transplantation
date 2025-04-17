import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic(name="test-get-method")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found():
    app = Sanic(name="test-get-method-not-found")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param():
    app = Sanic(name="test-get-method-query-param")

    @app.get("/get")
    async def get_method(request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'I am get method with param: test'

def test_get_method_empty_query_param():
    app = Sanic(name="test-get-method-empty-query-param")

    @app.get("/get")
    async def get_method(request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = app.test_client.get("/get?param=")
    assert response.status == 200
    assert response.text == 'I am get method with param: '