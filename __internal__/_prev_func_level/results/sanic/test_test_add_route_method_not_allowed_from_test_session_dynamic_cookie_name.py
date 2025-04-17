import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_allowed(app):
    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

def test_get_method_with_query_param(app):
    @app.get("/get")
    def get_method(request):
        return text(f"I am get method with query param: {request.args.get('param')}")

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == "I am get method with query param: test"