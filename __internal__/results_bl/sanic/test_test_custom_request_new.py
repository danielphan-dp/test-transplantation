import json
from io import BytesIO
from sanic import Sanic
from sanic.request import Request
from sanic.response import json_dumps, text
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

def test_get_method_with_query_params():
    request, response = app.test_client.get("/get?param=test")
    
    assert request.body == b""
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route():
    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404

def test_get_method_with_headers():
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/get", headers=headers)
    
    assert request.body == b""
    assert response.text == "I am get method"
    assert response.status == 200
    assert request.headers.get("Custom-Header") == "value"