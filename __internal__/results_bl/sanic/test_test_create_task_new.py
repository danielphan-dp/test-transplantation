import asyncio
import pytest
from threading import Event
from sanic.response import text

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/")
    assert response.body == b"I am get method"

@pytest.mark.asyncio
async def test_get_method_with_invalid_route(app):
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_concurrent_requests(app):
    async def make_request():
        request, response = await app.test_client.get("/")
        return response.body

    tasks = [make_request() for _ in range(10)]
    responses = await asyncio.gather(*tasks)
    assert all(response == b"I am get method" for response in responses)