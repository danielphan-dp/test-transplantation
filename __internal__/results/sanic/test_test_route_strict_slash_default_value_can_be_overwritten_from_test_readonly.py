import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_get_method")
    @app.get("/get")
    def handler(request):
        return text("I am get method")
    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_strict_slash(app):
    request, response = app.test_client.get("/get/")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/get_with_param")
    def handler_with_param(request):
        return text(f"I am get method with param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "I am get method with param: test"