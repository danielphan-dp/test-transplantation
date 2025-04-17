import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.asyncio
async def test_post_method(app):
    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    request, response = await app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_invalid_route(app):
    request, response = await app.test_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.asyncio
async def test_post_method_with_different_content_type(app):
    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    headers = {"content-type": "application/json"}
    request, response = await app.test_client.post("/post", headers=headers)
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_empty_body(app):
    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    request, response = await app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == 'I am post method'