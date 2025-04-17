import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method_response():
    app = Sanic("test_get_method")

    @app.get("/")
    async def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route():
    app = Sanic("test_get_method_invalid_route")

    @app.get("/valid")
    async def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params():
    app = Sanic("test_get_method_query_params")

    @app.get("/query")
    async def get(request):
        param = request.args.get('param', 'default')
        return text(f'Query param is {param}')

    request, response = app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == 'Query param is test'

    request, response = app.test_client.get("/query")
    assert response.status == 200
    assert response.text == 'Query param is default'