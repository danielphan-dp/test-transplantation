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

def test_get_method_returns_correct_response(json_app):
    @json_app.get("/test")
    def test_get(request):
        return text('I am get method')

    request = Mock(spec=Request)
    response = json_app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(json_app):
    response = json_app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_parameters(json_app):
    @json_app.get("/test")
    def test_get(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    response = json_app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'Query param: value'

def test_get_method_with_empty_query_parameters(json_app):
    @json_app.get("/test")
    def test_get(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    response = json_app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'Query param: none'