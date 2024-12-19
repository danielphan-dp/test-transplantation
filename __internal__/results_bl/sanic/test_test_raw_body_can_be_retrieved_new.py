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

def test_get_method_returns_correct_text(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    request = Mock(spec=Request)
    response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_parameters(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'Query param: test'

def test_get_method_empty_query_parameters(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'Query param: none'