import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

def test_get_method_without_decorator():
    app = Sanic("TestApp")

    class SimpleView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(SimpleView.as_view(), "/simple")
    request, response = app.test_client.get("/simple")
    assert response.text == "I am get method"

def test_get_method_with_empty_request():
    app = Sanic("TestApp")

    class EmptyRequestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(EmptyRequestView.as_view(), "/empty")
    request, response = app.test_client.get("/empty", headers={})
    assert response.text == "I am get method"

def test_get_method_with_query_params():
    app = Sanic("TestApp")

    class QueryParamView(HTTPMethodView):
        def get(self, request):
            return text("I am get method with query")

    app.add_route(QueryParamView.as_view(), "/query")
    request, response = app.test_client.get("/query?param=value")
    assert response.text == "I am get method with query"

def test_get_method_with_invalid_route():
    app = Sanic("TestApp")

    class InvalidRouteView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(InvalidRouteView.as_view(), "/invalid")
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_custom_header():
    app = Sanic("TestApp")

    class CustomHeaderView(HTTPMethodView):
        def get(self, request):
            return text("I am get method with custom header")

    app.add_route(CustomHeaderView.as_view(), "/custom-header")
    request, response = app.test_client.get("/custom-header", headers={"X-Custom-Header": "value"})
    assert response.text == "I am get method with custom header"