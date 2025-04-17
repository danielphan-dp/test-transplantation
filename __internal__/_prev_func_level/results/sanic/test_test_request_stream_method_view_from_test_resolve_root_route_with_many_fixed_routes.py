import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

def test_get_method_response(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(TestView.as_view(), "/test_get")

    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_with_query_params(app):
    class QueryParamView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'Query param is {param}')

    app.add_route(QueryParamView.as_view(), "/query_param")

    request, response = app.test_client.get("/query_param?param=test")
    assert response.status == 200
    assert response.text == "Query param is test"

    request, response = app.test_client.get("/query_param")
    assert response.status == 200
    assert response.text == "Query param is default"