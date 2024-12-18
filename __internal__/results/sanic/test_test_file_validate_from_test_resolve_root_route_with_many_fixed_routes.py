import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.route("/get", methods=["GET"])
    def get_method(request: Request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.route("/get_with_params", methods=["GET"])
    def get_with_params(request: Request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.status == 200
    assert response.text == "I am get method with param: test"

def test_get_method_without_query_params(app):
    @app.route("/get_with_params", methods=["GET"])
    def get_with_params(request: Request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/get_with_params")
    assert response.status == 200
    assert response.text == "I am get method with param: default"