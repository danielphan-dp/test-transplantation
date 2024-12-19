import json
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")

    assert response.body == b'I am get method'
    assert response.status == 200

def test_get_method_with_query_params(app):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get?param=test")

    assert response.body == b'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")

    assert response.status == 404

def test_get_method_with_headers(app):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/get", headers=headers)

    assert response.body == b'I am get method'
    assert response.status == 200

def test_get_method_empty_response(app):
    @app.get("/empty")
    async def handler(request):
        return text('')

    request, response = app.test_client.get("/empty")

    assert response.body == b''
    assert response.status == 200