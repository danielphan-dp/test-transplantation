import json
from sanic import Sanic
from sanic.response import text
import pytest

app = Sanic(name="Test")

@app.route("/get")
async def get_handler(request):
    return text("I am get method")

def test_get_method():
    request, response = app.test_client.get("/get")
    
    assert request.body == b""
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route():
    request, response = app.test_client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_headers():
    headers = {"X-Custom-Header": "value"}
    request, response = app.test_client.get("/get", headers=headers)
    
    assert request.headers.get("X-Custom-Header") == "value"
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_params():
    request, response = app.test_client.get("/get?param=value")
    
    assert request.args.get("param") == "value"
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_empty_query_params():
    request, response = app.test_client.get("/get?")
    
    assert request.args == {}
    assert response.text == "I am get method"
    assert response.status == 200