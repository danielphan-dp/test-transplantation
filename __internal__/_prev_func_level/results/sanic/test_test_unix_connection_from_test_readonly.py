import os
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic(name="test")
    return app

def test_get_method(app):
    @app.get("/")
    def handler(request: Request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/")
    def handler(request: Request):
        return text('I am get method', headers={'X-Custom-Header': 'value'})

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'value'

def test_get_method_with_query_params(app):
    @app.get("/greet")
    def handler(request: Request):
        name = request.args.get('name', 'World')
        return text(f'Hello, {name}!')

    request, response = app.test_client.get("/greet?name=Alice")
    assert response.status == 200
    assert response.text == 'Hello, Alice!'

    request, response = app.test_client.get("/greet")
    assert response.status == 200
    assert response.text == 'Hello, World!'