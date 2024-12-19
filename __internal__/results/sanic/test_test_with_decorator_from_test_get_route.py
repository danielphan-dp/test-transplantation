import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/test")
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    class QueryView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"Received param: {param}")

    app.add_route(QueryView.as_view(), "/query")
    request, response = app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_with_empty_query_param(app):
    class EmptyQueryView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"Received param: {param}")

    app.add_route(EmptyQueryView.as_view(), "/empty_query")
    request, response = app.test_client.get("/empty_query?param=")
    assert response.status == 200
    assert response.text == "Received param: "