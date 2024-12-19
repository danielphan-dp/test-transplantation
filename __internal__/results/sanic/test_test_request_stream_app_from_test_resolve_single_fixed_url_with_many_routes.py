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
async def test_head_request(app):
    request, response = await app.test_client.head("/head")
    assert response.status == 200
    assert response.text == ""
    assert response.headers['method'] == 'HEAD'

@pytest.mark.asyncio
async def test_head_request_with_nonexistent_route(app):
    request, response = await app.test_client.head("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_head_request_with_custom_headers(app):
    request, response = await app.test_client.head("/head", headers={"Custom-Header": "Value"})
    assert response.status == 200
    assert response.headers['method'] == 'HEAD'
    assert response.headers.get("Custom-Header") is None

@pytest.mark.asyncio
async def test_head_request_empty_body(app):
    request, response = await app.test_client.head("/head")
    assert response.status == 200
    assert response.text == ""
    assert response.headers['Content-Length'] == '0'