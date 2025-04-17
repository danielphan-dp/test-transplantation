import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic(name="get-method-test")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found():
    app = Sanic(name="get-method-not-found-test")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param():
    app = Sanic(name="get-method-query-param-test")

    @app.get("/get")
    async def get_method(request):
        return text(f'I am get method with param: {request.args.get("param", "None")}')

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'I am get method with param: test'