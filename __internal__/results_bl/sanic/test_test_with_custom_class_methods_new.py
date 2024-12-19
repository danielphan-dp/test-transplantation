import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

def test_get_method_without_internal_method(app):
    class SimpleView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(SimpleView.as_view(), "/simple")
    request, response = app.test_client.get("/simple")
    assert response.text == 'I am get method'

def test_get_method_with_no_request(app):
    class NoRequestView(HTTPMethodView):
        def get(self, request):
            return text('I am get method with no request')

    app.add_route(NoRequestView.as_view(), "/no_request")
    request, response = app.test_client.get("/no_request")
    assert response.text == 'I am get method with no request'

def test_get_method_with_different_path(app):
    class DifferentPathView(HTTPMethodView):
        def get(self, request):
            return text('I am get method at a different path')

    app.add_route(DifferentPathView.as_view(), "/different")
    request, response = app.test_client.get("/different")
    assert response.text == 'I am get method at a different path'

def test_get_method_with_query_parameters(app):
    class QueryParamView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'I am get method with param: {param}')

    app.add_route(QueryParamView.as_view(), "/query")
    request, response = app.test_client.get("/query?param=test")
    assert response.text == 'I am get method with param: test'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404