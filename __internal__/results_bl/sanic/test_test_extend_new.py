import json
from functools import partial
from unittest.mock import Mock
import pytest
from sanic import Request, Sanic
from sanic.exceptions import SanicException
from sanic.response import text, json as json_response
from sanic.response.types import JSONResponse

@pytest.fixture
def json_app():
    app = Sanic("TestApp")
    return app

def test_get_method(json_app):
    @json_app.get("/get-method")
    async def handler_get(request: Request):
        return text('I am get method')

    _, resp = json_app.test_client.get("/get-method")
    assert resp.body == b'I am get method'

def test_get_method_empty_request(json_app):
    @json_app.get("/get-method-empty")
    async def handler_get_empty(request: Request):
        return text('I am get method')

    _, resp = json_app.test_client.get("/get-method-empty", data={})
    assert resp.body == b'I am get method'

def test_get_method_invalid_route(json_app):
    with pytest.raises(SanicException):
        _, resp = json_app.test_client.get("/invalid-route")