import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('unquote', [True, False, None])
@pytest.mark.asyncio
async def test_get_method(app, unquote):
    response = await app.test_client.get('/')
    assert response.text == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_with_invalid_route(app):
    response = await app.test_client.get('/invalid')
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    response = await app.test_client.get('/?param=value')
    assert response.text == 'I am get method'  # Assuming the method does not change with query params

@pytest.mark.asyncio
async def test_get_method_with_headers(app):
    response = await app.test_client.get('/', headers={'Custom-Header': 'value'})
    assert response.text == 'I am get method'  # Assuming headers do not affect the response

@pytest.mark.asyncio
async def test_get_method_with_empty_request(app):
    response = await app.test_client.get('/')
    assert response.text == 'I am get method'  # Testing with an empty request body