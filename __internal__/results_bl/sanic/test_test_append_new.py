import json
from functools import partial
from unittest.mock import Mock
import pytest
from sanic import Request, Sanic
from sanic.exceptions import SanicException
from sanic.response import text
from sanic.response.types import JSONResponse

@pytest.fixture
def json_app():
    app = Sanic("test_app")
    return app

def test_get_method(json_app):
    @json_app.get("/get-method")
    async def handler_get(request: Request):
        return text('I am get method')

    _, resp = json_app.test_client.get("/get-method")
    assert resp.body == b'I am get method'

def test_get_method_not_found(json_app):
    @json_app.get("/get-method")
    async def handler_get(request: Request):
        return text('I am get method')

    _, resp = json_app.test_client.get("/non-existent-endpoint")
    assert resp.status == 404

def test_get_method_with_query_param(json_app):
    @json_app.get("/get-method")
    async def handler_get(request: Request):
        return text(f'I am get method with param: {request.args.get("param", "")}')

    _, resp = json_app.test_client.get("/get-method?param=test")
    assert resp.body == b'I am get method with param: test'