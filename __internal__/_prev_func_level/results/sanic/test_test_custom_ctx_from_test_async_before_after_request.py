import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic("Test")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")

    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_invalid_route():
    app = Sanic("Test")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid_route")

    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_param():
    app = Sanic("Test")

    @app.get("/get")
    async def get_method(request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = app.test_client.get("/get?param=test")

    assert response.text == 'I am get method with param: test'
    assert response.status == 200

def test_get_method_without_query_param():
    app = Sanic("Test")

    @app.get("/get")
    async def get_method(request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = app.test_client.get("/get")

    assert response.text == 'I am get method with param: default'
    assert response.status == 200