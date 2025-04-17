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

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_request_object(app):
    request, response = app.test_client.get("/get")
    assert bool(request)

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_with_query")
    def handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get_with_query?param=test")
    assert response.text == "Query param: test"
    assert response.status == 200

def test_get_method_without_query_params(app):
    @app.get("/get_with_query")
    def handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get_with_query")
    assert response.text == "Query param: none"
    assert response.status == 200