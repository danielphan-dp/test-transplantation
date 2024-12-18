import pytest
from sanic import Sanic, response
from sanic.request import Request

app = Sanic("test_app")

@app.get("/get")
def get_method(request: Request):
    return response.text('I am get method')

def test_get_method():
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route():
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_header():
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_query_params():
    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_empty_request():
    request, response = app.test_client.get("/get", data={})
    assert response.text == 'I am get method'
    assert response.status == 200