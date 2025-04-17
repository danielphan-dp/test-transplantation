import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.fixture
def client(app):
    return app.test_client

@pytest.mark.asyncio
async def test_get_method(client):
    class TestView:
        def get(self, request):
            return text('I am get method')

    app.add_route(TestView().get, "/test_get")

    request, response = await client.get("/test_get")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_not_found(client):
    request, response = await client.get("/non_existent_route")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_param(client):
    class TestView:
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'Param is {param}')

    app.add_route(TestView().get, "/test_get_with_param")

    request, response = await client.get("/test_get_with_param?param=value")
    assert response.status == 200
    assert response.text == 'Param is value'

    request, response = await client.get("/test_get_with_param")
    assert response.status == 200
    assert response.text == 'Param is default'