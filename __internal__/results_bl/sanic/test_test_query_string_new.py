import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get")
async def get_handler(request):
    return text('I am get method')

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_with_query_string(app):
    request, response = app.test_client.get("/get", params=[("param1", "value1")])
    assert request.args.get("param1") == "value1"
    assert response.text == 'I am get method'

def test_get_with_no_query_string(app):
    request, response = app.test_client.get("/get")
    assert request.args == {}
    assert response.text == 'I am get method'

def test_get_with_multiple_query_strings(app):
    request, response = app.test_client.get("/get", params=[("param1", "value1"), ("param2", "value2")])
    assert request.args.get("param1") == "value1"
    assert request.args.get("param2") == "value2"
    assert response.text == 'I am get method'

def test_get_with_empty_query_string(app):
    request, response = app.test_client.get("/get", params=[("param1", "")])
    assert request.args.get("param1") == ""
    assert response.text == 'I am get method'