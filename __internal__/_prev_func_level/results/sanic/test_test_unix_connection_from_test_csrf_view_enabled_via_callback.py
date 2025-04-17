import os
import pytest
from sanic import Sanic
from sanic.request import Request
from sanic.response import text

app = Sanic(name="test")

@app.get("/")
def handler(request: Request):
    return text('I am get method')

@pytest.mark.asyncio
async def test_get_method():
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_invalid_route():
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_custom_header():
    request, response = await app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("Custom-Header") is None  # Ensure custom header is not returned

@pytest.mark.asyncio
async def test_get_method_with_query_params():
    request, response = await app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure query params do not affect response

@pytest.mark.asyncio
async def test_get_method_with_unexpected_method():
    request, response = await app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text