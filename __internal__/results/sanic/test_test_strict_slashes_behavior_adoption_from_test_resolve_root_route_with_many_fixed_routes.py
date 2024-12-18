import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get/")
    assert response.status == 404

def test_get_method_with_strict_slashes(app):
    app.strict_slashes = True

    @app.get("/strict")
    def strict_handler(request):
        return text("Strict slashes")

    request, response = app.test_client.get("/strict")
    assert response.status == 200

    request, response = app.test_client.get("/strict/")
    assert response.status == 404

def test_get_method_with_non_strict_slashes(app):
    app.strict_slashes = False

    @app.get("/non-strict")
    def non_strict_handler(request):
        return text("Non-strict slashes")

    request, response = app.test_client.get("/non-strict")
    assert response.status == 200

    request, response = app.test_client.get("/non-strict/")
    assert response.status == 200

def test_get_method_with_query_parameters(app):
    @app.get("/query")
    def query_handler(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == "Query param: test"