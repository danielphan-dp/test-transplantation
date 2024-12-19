import os
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

app = Sanic(name="test")

@app.get("/get")
def get_method(request: Request):
    return text('I am get method')

@pytest.mark.asyncio
async def test_get_method_success():
    async with app.test_client() as client:
        response = await client.get('/get')
        assert response.status == 200
        assert response.text == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_invalid_route():
    async with app.test_client() as client:
        response = await client.get('/invalid')
        assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params():
    async with app.test_client() as client:
        response = await client.get('/get?param=value')
        assert response.status == 200
        assert response.text == 'I am get method'  # Assuming the method does not change behavior with params

@pytest.mark.asyncio
async def test_get_method_empty_request():
    async with app.test_client() as client:
        response = await client.get('/get')
        assert response.status == 200
        assert response.text == 'I am get method'  # Testing with no additional data in request

@pytest.mark.asyncio
async def test_get_method_with_headers():
    async with app.test_client() as client:
        response = await client.get('/get', headers={'Custom-Header': 'value'})
        assert response.status == 200
        assert response.text == 'I am get method'  # Ensure headers do not affect response content