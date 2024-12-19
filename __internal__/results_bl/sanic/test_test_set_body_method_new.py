import json
from functools import partial
from unittest.mock import Mock
import pytest
from sanic import Request, Sanic
from sanic.exceptions import SanicException
from sanic.response import json as sanic_json
from sanic.response.types import JSONResponse

@pytest.fixture
def json_app():
    app = Sanic("TestApp")
    return app

def test_get_method(json_app):
    @json_app.get("/get")
    def get_method(request):
        return text('I am get method')

    _, resp = json_app.test_client.get("/get")
    assert resp.text == 'I am get method'

def test_get_method_with_invalid_route(json_app):
    _, resp = json_app.test_client.get("/invalid")
    assert resp.status == 404

def test_get_method_with_query_params(json_app):
    @json_app.get("/get")
    def get_method(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    _, resp = json_app.test_client.get("/get?param=test")
    assert resp.text == 'Query param: test'

def test_get_method_with_empty_query_params(json_app):
    @json_app.get("/get")
    def get_method(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    _, resp = json_app.test_client.get("/get")
    assert resp.text == 'Query param: none'