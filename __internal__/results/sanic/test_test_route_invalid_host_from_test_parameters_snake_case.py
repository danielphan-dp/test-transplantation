import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/test-get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/test-get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/test-get-query")
    def handler(request):
        return text(f"Query param received: {request.args.get('param')}")

    request, response = app.test_client.get("/test-get-query?param=test")
    assert response.status == 200
    assert response.text == "Query param received: test"

def test_get_method_with_empty_query_params(app):
    @app.get("/test-get-empty-query")
    def handler(request):
        return text("No query param")

    request, response = app.test_client.get("/test-get-empty-query")
    assert response.status == 200
    assert response.text == "No query param"