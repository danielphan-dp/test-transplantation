import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("test_app")

@app.get("/get")
def get_method(request):
    return text('I am get method')

def test_get_method_response():
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route():
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_headers():
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None

def test_get_method_with_query_params():
    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_different_accept_header():
    header_value = "application/json"
    request, response = app.test_client.get("/get", headers={"Accept": header_value})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"