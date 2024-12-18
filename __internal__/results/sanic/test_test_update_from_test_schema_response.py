import json
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get-method")
    async def handler_get(request: Request):
        return text('I am get method')

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get-method")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get-method?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # No change in response for query params

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get-method", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'  # No change in response for headers

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get-method", data={})
    assert response.status == 200
    assert response.text == 'I am get method'  # No change in response for empty data