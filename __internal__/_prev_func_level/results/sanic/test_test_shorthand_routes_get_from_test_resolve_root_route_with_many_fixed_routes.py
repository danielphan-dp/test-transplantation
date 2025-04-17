import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_not_allowed(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405

def test_get_method_with_query_params(app):
    @app.get("/get")
    def handler_with_params(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get?param=test")
    assert response.text == "Received param: test"

def test_get_method_with_no_query_params(app):
    @app.get("/get")
    def handler_with_params(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get")
    assert response.text == "Received param: default"