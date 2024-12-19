import uuid
import pytest
from sanic import Sanic
from sanic.response import text, json
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/get")
    async def get(request):
        return text('I am get method')
    return app

def test_get_method_response(app):
    _, resp = app.test_client.get("/get")
    assert resp.text == 'I am get method'

def test_get_method_invalid_route(app):
    _, resp = app.test_client.get("/invalid")
    assert resp.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    async def get_with_params(request):
        return json({"param": request.args.get("param")})

    _, resp = app.test_client.get("/get_with_params?param=test")
    assert resp.json["param"] == "test"

def test_get_method_empty_request(app):
    @app.get("/get_empty")
    async def get_empty(request):
        return text('Empty request')

    _, resp = app.test_client.get("/get_empty")
    assert resp.text == 'Empty request'