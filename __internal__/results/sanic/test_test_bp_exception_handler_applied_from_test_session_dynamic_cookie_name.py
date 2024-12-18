import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get_with_param")
    def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_no_query_params(app):
    request, response = app.test_client.get("/get_with_param")
    assert response.status == 200
    assert response.text == "Received param: default"