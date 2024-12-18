import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/test")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    @app.get("/test")
    def get_method_with_param(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == "I am get method with param: value"

def test_get_method_without_query_param(app):
    @app.get("/test")
    def get_method_with_param(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method with param: default"