import json
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_returns_correct_response(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    _, resp = app.test_client.get("/get")
    assert resp.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    _, resp = app.test_client.get("/invalid")
    assert resp.status == 404

def test_get_method_with_query_parameters(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text(f'Query param: {request.args.get("param", "not found")}')

    _, resp = app.test_client.get("/get?param=test")
    assert resp.text == 'Query param: test'

def test_get_method_with_no_query_parameters(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text(f'Query param: {request.args.get("param", "not found")}')

    _, resp = app.test_client.get("/get")
    assert resp.text == 'Query param: not found'