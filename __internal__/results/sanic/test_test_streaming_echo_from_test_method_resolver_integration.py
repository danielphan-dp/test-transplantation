import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.asyncio
async def test_post_method():
    app = Sanic(name="Test")

    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    request, response = await app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_data():
    app = Sanic(name="Test")

    @app.post("/post")
    async def post_handler(request):
        data = request.json
        return text(f'I am post method with data: {data}')

    request, response = await app.test_client.post("/post", json={"key": "value"})
    assert response.status == 200
    assert response.text == 'I am post method with data: {"key": "value"}'

@pytest.mark.asyncio
async def test_post_method_invalid_route():
    app = Sanic(name="Test")

    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    request, response = await app.test_client.post("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

@pytest.mark.asyncio
async def test_post_method_with_empty_body():
    app = Sanic(name="Test")

    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    request, response = await app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == 'I am post method'