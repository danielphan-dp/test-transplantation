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

@pytest.mark.asyncio
async def test_head_response(app):
    request, response = await app.test_client.head("/head")
    assert response.status == 200
    assert response.text == ""
    assert response.headers['method'] == 'HEAD'

@pytest.mark.asyncio
async def test_head_with_invalid_route(app):
    request, response = await app.test_client.head("/invalid")
    assert response.status == 404

@pytest.mark.asyncio
async def test_head_with_custom_headers(app):
    @app.head("/custom")
    async def custom_head(request):
        return text('', headers={'X-Custom-Header': 'CustomValue'})
    
    request, response = await app.test_client.head("/custom")
    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'CustomValue'