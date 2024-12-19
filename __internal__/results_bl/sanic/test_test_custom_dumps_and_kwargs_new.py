import json
from functools import partial
from unittest.mock import Mock
import pytest
from sanic import Request, Sanic
from sanic.exceptions import SanicException
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(json_app):
    @json_app.get("/get-method")
    async def handle_get(request: Request):
        return text('I am get method')

    _, resp = json_app.test_client.get("/get-method")
    assert resp.body == b'I am get method'

def test_get_method_invalid_route(json_app):
    _, resp = json_app.test_client.get("/invalid-route")
    assert resp.status == 404

def test_get_method_with_query_param(json_app):
    @json_app.get("/get-method")
    async def handle_get(request: Request):
        return text(f'I am get method with param: {request.args.get("param", "none")}')

    _, resp = json_app.test_client.get("/get-method?param=test")
    assert resp.body == b'I am get method with param: test'