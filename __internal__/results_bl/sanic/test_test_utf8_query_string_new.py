import json
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get")
async def get_method(request):
    return text('I am get method')

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_query_string(app):
    request, response = app.test_client.get("/get", params=[("utf8", "✓")])
    assert request.args.get("utf8") == "✓"

def test_get_method_with_empty_query_string(app):
    request, response = app.test_client.get("/get", params=[("utf8", "")])
    assert request.args.get("utf8") == ""

def test_get_method_with_non_utf8_query_string(app):
    request, response = app.test_client.get("/get", params=[("utf8", "invalid_char_☃")])
    assert request.args.get("utf8") == "invalid_char_☃"