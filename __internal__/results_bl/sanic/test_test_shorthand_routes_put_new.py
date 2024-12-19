import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get")
    def handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get?param=test")
    assert response.text == "Query param: test"
    assert response.status == 200

def test_get_method_with_empty_query_params(app):
    @app.get("/get")
    def handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get?param=")
    assert response.text == "Query param: "
    assert response.status == 200

def test_get_method_invalid_method(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.post("/get")
    assert response.status == 405