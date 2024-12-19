import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_with_invalid_route(app):
    _, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get_with_params", methods=["GET"])
    def get_with_params(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    _, response = app.test_client.get("/get_with_params?param=test")
    assert response.status == 200
    assert response.body == b'Query param: test'

def test_get_method_with_no_query_params(app):
    @app.route("/get_with_no_params", methods=["GET"])
    def get_with_no_params(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    _, response = app.test_client.get("/get_with_no_params")
    assert response.status == 200
    assert response.body == b'Query param: none'