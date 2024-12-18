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

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.body == b"I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert b"Requested URL /nonexistent not found" in response.body

def test_get_method_with_query_param(app):
    @app.route("/get")
    def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get?param=test")
    assert response.body == b"Received param: test"

def test_get_method_empty_query_param(app):
    @app.route("/get")
    def get_with_empty_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get?param=")
    assert response.body == b"Received param: "