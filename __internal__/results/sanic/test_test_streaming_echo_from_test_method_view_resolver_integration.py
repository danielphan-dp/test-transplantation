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
async def test_post_method_with_invalid_data():
    app = Sanic(name="Test")

    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    request, response = await app.test_client.post("/post", data="invalid data")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_empty_body():
    app = Sanic(name="Test")

    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    request, response = await app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == 'I am post method'