import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get", methods=["GET"])
    def get(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_invalid_method(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405

def test_get_method_with_query_param(app):
    @app.route("/get_with_param", methods=["GET"])
    def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Received param: test"

def test_get_method_without_query_param(app):
    request, response = app.test_client.get("/get_with_param")
    assert response.text == "Received param: default"