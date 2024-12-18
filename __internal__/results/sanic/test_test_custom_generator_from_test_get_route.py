import pytest
from sanic import Sanic, response
from sanic.request import Request

app = Sanic("test_app")

@app.get("/get_method")
async def get_method(request: Request):
    return response.text('I am get method')

@pytest.mark.asyncio
async def test_get_method_success():
    request, response = await app.test_client.get("/get_method")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_invalid_route():
    request, response = await app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_headers():
    request, response = await app.test_client.get("/get_method", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'