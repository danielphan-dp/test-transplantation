import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.head("/head")
    async def head(request):
        return text('', headers={'method': 'HEAD'})

    return app

def test_head_request(app):
    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.text == ""
    assert response.headers['method'] == 'HEAD'

def test_head_request_with_invalid_route(app):
    request, response = app.test_client.head("/invalid")
    assert response.status == 404

def test_head_request_with_custom_headers(app):
    @app.head("/custom")
    async def custom_head(request):
        return text('', headers={'Custom-Header': 'Value'})

    request, response = app.test_client.head("/custom")
    assert response.status == 200
    assert response.headers['Custom-Header'] == 'Value'

def test_head_request_empty_body(app):
    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.text == ''
    assert response.content_length == 0

def test_head_request_with_query_params(app):
    @app.head("/query")
    async def query_head(request):
        return text('', headers={'Query-Param': request.args.get('param', 'default')})

    request, response = app.test_client.head("/query?param=test")
    assert response.status == 200
    assert response.headers['Query-Param'] == 'test'