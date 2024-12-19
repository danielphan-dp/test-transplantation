import json
import pytest
from sanic import Sanic, Request
from sanic.exceptions import SanicException
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("TestApp")
    return app

def test_get_method_returns_correct_response(json_app):
    @json_app.get("/test")
    def test_get(request):
        return text('I am get method')

    request, response = json_app.test_client.get("/test")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_parameters(json_app):
    @json_app.get("/test")
    def test_get(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = json_app.test_client.get("/test?param=value")
    assert response.text == 'Query param: value'
    assert response.status == 200

def test_get_method_with_empty_query_parameters(json_app):
    @json_app.get("/test")
    def test_get(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = json_app.test_client.get("/test?param=")
    assert response.text == 'Query param: '
    assert response.status == 200

def test_get_method_with_headers(json_app):
    @json_app.get("/test")
    def test_get(request):
        return text(f'Header value: {request.headers.get("X-Custom-Header", "none")}')

    request, response = json_app.test_client.get("/test", headers={"X-Custom-Header": "value"})
    assert response.text == 'Header value: value'
    assert response.status == 200

def test_get_method_with_no_headers(json_app):
    @json_app.get("/test")
    def test_get(request):
        return text(f'Header value: {request.headers.get("X-Custom-Header", "none")}')

    request, response = json_app.test_client.get("/test")
    assert response.text == 'Header value: none'
    assert response.status == 200