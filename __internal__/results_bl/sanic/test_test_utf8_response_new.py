import json
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.route("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_empty_request(app):
    @app.route("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={'Content-Length': '0'})
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'