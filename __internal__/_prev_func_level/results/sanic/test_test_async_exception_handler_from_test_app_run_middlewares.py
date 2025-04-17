import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/test")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_param(app):
    @app.get("/test_query")
    def get_method_with_query(request):
        param = request.args.get("param", "default")
        return text(f"Query param is {param}")

    request, response = app.test_client.get("/test_query?param=value")
    assert response.status == 200
    assert response.text == "Query param is value"

def test_get_method_with_no_query_param(app):
    @app.get("/test_query_default")
    def get_method_with_default_query(request):
        param = request.args.get("param", "default")
        return text(f"Query param is {param}")

    request, response = app.test_client.get("/test_query_default")
    assert response.status == 200
    assert response.text == "Query param is default"