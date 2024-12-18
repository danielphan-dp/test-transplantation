import pytest
from sanic import Sanic, response
from sanic.request import Request

app = Sanic("test_app")

@app.get("/test")
async def get_method(request):
    return response.text('I am get method')

def test_get_method_response():
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_custom_header():
    request, response = app.test_client.get("/test", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route():
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params():
    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'