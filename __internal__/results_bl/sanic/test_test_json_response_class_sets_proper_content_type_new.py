import json
from functools import partial
from unittest.mock import Mock
import pytest
from sanic import Request, Sanic
from sanic.exceptions import SanicException
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_returns_text_response(app):
    @app.get("/get-method")
    async def handler(request: Request):
        return text('I am get method')

    _, resp = app.test_client.get("/get-method")
    assert resp.status == 200
    assert resp.text == 'I am get method'
    assert resp.headers["content-type"] == "text/plain; charset=utf-8"

def test_get_method_invalid_route(app):
    _, resp = app.test_client.get("/invalid-route")
    assert resp.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get-method")
    async def handler(request: Request):
        return text(f'Query param: {request.args.get("param", "none")}')

    _, resp = app.test_client.get("/get-method?param=test")
    assert resp.status == 200
    assert resp.text == 'Query param: test'