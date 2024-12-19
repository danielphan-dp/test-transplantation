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

def test_get_method(json_app):
    @json_app.get("/get-method")
    async def handle_get(request: Request):
        return text('I am get method')

    _, resp = json_app.test_client.get("/get-method")

    assert resp.body == b'I am get method'
    assert resp.status == 200

def test_get_method_with_invalid_route(json_app):
    _, resp = json_app.test_client.get("/invalid-route")

    assert resp.status == 404

def test_get_method_with_query_params(json_app):
    @json_app.get("/get-method-with-params")
    async def handle_get_with_params(request: Request):
        return text(f'Query param: {request.args.get("param", "none")}')

    _, resp = json_app.test_client.get("/get-method-with-params?param=test")

    assert resp.body == b'Query param: test'
    assert resp.status == 200

def test_get_method_with_no_query_params(json_app):
    @json_app.get("/get-method-no-params")
    async def handle_get_no_params(request: Request):
        return text(f'Query param: {request.args.get("param", "none")}')

    _, resp = json_app.test_client.get("/get-method-no-params")

    assert resp.body == b'Query param: none'
    assert resp.status == 200