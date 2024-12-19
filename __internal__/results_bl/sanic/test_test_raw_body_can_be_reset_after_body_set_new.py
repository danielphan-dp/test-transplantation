import json
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("TestApp")
    return app

def test_get_method_returns_correct_response(json_app):
    @json_app.get("/test")
    def test_get(request: Request):
        return text('I am get method')

    _, resp = json_app.test_client.get("/test")
    assert resp.text == 'I am get method'

def test_get_method_with_invalid_route(json_app):
    _, resp = json_app.test_client.get("/invalid")
    assert resp.status == 404

def test_get_method_with_query_parameters(json_app):
    @json_app.get("/test")
    def test_get(request: Request):
        return text(f'Query param: {request.args.get("param", "none")}')

    _, resp = json_app.test_client.get("/test?param=value")
    assert resp.text == 'Query param: value'

def test_get_method_with_empty_query_parameters(json_app):
    @json_app.get("/test")
    def test_get(request: Request):
        return text(f'Query param: {request.args.get("param", "none")}')

    _, resp = json_app.test_client.get("/test?param=")
    assert resp.text == 'Query param: '