import base64
import logging
import json
import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic(name="Test")

@app.route("/get")
def get_method(request):
    return text('I am get method')

def test_get_method_basic():
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_not_found():
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params():
    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_empty_request():
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_invalid_route():
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404