import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/test_get")
def test_get_method(request):
    return text('I am get method')

def test_get_method_response(app):
    request, response = app.test_client.get("/test_get")
    assert response.body == b'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_empty_request(app):
    request, response = app.test_client.get("/test_get", headers={})
    assert response.body == b'I am get method'

def test_get_method_with_additional_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/test_get", headers=headers)
    assert response.body == b'I am get method'