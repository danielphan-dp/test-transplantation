import os
import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('url', ['/test', '/another_test'])
def test_get_method(app, url):
    @app.get(url)
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(url)
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get('/invalid_route')
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get('/test_with_params')
    async def handler(request):
        return text(f'Query param: {request.args.get("param", "not provided")}')

    request, response = app.test_client.get('/test_with_params?param=value')
    
    assert response.status == 200
    assert response.text == 'Query param: value'