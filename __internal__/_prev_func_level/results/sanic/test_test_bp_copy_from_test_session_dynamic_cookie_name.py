import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    class TestView:
        def get(self, request):
            return text('I am get method')

    app.add_route(TestView().get, "/test_get")

    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    class TestView:
        def get(self, request):
            return text(f"Query param value: {request.args.get('param', 'not found')}")

    app.add_route(TestView().get, "/test_get_query")

    request, response = app.test_client.get("/test_get_query?param=value")
    assert response.status == 200
    assert response.text == "Query param value: value"

def test_get_method_with_empty_query_params(app):
    class TestView:
        def get(self, request):
            return text(f"Query param value: {request.args.get('param', 'not found')}")

    app.add_route(TestView().get, "/test_get_empty_query")

    request, response = app.test_client.get("/test_get_empty_query")
    assert response.status == 200
    assert response.text == "Query param value: not found"