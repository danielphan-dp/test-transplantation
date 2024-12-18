import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    @app.route("/get")
    def get_method_with_param(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/get?param=test")
    assert response.text == "I am get method with param: test"

def test_get_method_with_empty_query_param(app):
    @app.route("/get")
    def get_method_with_empty_param(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/get?param=")
    assert response.text == "I am get method with param: "