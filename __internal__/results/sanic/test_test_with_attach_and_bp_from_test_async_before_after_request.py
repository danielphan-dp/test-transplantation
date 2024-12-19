import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_with_different_response(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("Different response")

    app.add_route(DummyView.as_view(), "/different")

    request, response = app.test_client.get("/different")
    assert response.text == "Different response"

def test_get_method_empty_response(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("")

    app.add_route(DummyView.as_view(), "/empty")

    request, response = app.test_client.get("/empty")
    assert response.text == ""

def test_get_method_not_found(app):
    request, response = app.test_client.get("/not_found")
    assert response.status == 404
    assert "Requested URL /not_found not found" in response.text

def test_get_method_with_query_param(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text(f"Query param: {request.args.get('param', 'none')}")

    app.add_route(DummyView.as_view(), "/query")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param: test"