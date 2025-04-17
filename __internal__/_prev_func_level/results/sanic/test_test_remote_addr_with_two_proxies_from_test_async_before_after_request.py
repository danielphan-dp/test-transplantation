import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_header(app):
    headers = {"Custom-Header": "TestValue"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_empty_response(app):
    @app.route("/empty")
    def empty_method(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""
    assert response.status == 200

def test_get_method_with_query_params(app):
    @app.route("/get_with_params")
    def get_with_params(request):
        param = request.args.get("param", "default")
        return text(f"Param value: {param}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.text == "Param value: test"
    assert response.status == 200

    request, response = app.test_client.get("/get_with_params")
    assert response.text == "Param value: default"
    assert response.status == 200