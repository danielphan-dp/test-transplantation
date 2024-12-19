import pytest
from sanic.blueprints import Blueprint
from sanic.constants import HTTP_METHODS
from sanic.request import Request
from sanic.response import HTTPResponse, text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    from sanic import Sanic
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    class DummyView(HTTPMethodView, attach=app, uri="/"):
        def get(self, request):
            return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_empty_request(app):
    class DummyView(HTTPMethodView, attach=app, uri="/empty"):
        def get(self, request):
            return text("Empty request")

    request, response = app.test_client.get("/empty")
    assert response.text == "Empty request"

def test_get_method_with_query_params(app):
    class DummyView(HTTPMethodView, attach=app, uri="/query"):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"Query param is: {param}")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param is: test"

def test_get_method_with_no_query_params(app):
    class DummyView(HTTPMethodView, attach=app, uri="/query-default"):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"Query param is: {param}")

    request, response = app.test_client.get("/query-default")
    assert response.text == "Query param is: default"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404