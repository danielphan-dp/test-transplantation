import pytest
from sanic import Sanic, response
from sanic.request import Request

app = Sanic("test_app")

@app.get("/get")
async def get_method(request: Request):
    return response.text('I am get method')

def test_get_method_success():
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route():
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_headers():
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_empty_request():
    request, response = app.test_client.get("/get", data="")
    assert response.status == 200
    assert response.text == 'I am get method'