import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get_with_params", methods=["GET"])
    def get_with_params(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.status == 200
    assert response.text == 'Query param: test'

def test_get_method_empty_query_params(app):
    @app.route("/get_with_empty_params", methods=["GET"])
    def get_with_empty_params(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/get_with_empty_params")
    assert response.status == 200
    assert response.text == 'Query param: none'