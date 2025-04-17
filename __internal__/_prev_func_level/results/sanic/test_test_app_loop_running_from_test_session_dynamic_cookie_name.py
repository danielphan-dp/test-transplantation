import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_response_empty(app):
    @app.get("/get_empty")
    async def handler(request):
        return text('')

    request, response = app.test_client.get("/get_empty")
    assert response.text == ''

def test_get_method_response_not_found(app):
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text

def test_get_method_response_with_query_param(app):
    @app.get("/get_with_param")
    async def handler(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == 'Query param: test'