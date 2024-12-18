import os
import pytest
from sanic import Sanic
from sanic.request import Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic(name="test")
    return app

def test_get_method(app):
    @app.get("/get")
    def handler(request: Request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_unexpected_method(app):
    @app.get("/get")
    def handler(request: Request):
        return text('I am get method')

    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

def test_get_method_with_query_parameters(app):
    @app.get("/get")
    def handler(request: Request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == "Query param: test"

def test_get_method_with_no_query_parameters(app):
    @app.get("/get")
    def handler(request: Request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "Query param: none"