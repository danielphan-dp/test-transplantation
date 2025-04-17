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
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/test")

    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"

def test_get_method_with_different_path(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method with different path")

    app.add_route(TestView.as_view(), "/another_test")

    request, response = app.test_client.get("/another_test")
    assert response.text == "I am get method with different path"

def test_get_method_with_query_param(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            param = request.args.get("param", "default")
            return text(f"Received param: {param}")

    app.add_route(TestView.as_view(), "/query_test")

    request, response = app.test_client.get("/query_test?param=test_value")
    assert response.text == "Received param: test_value"

def test_get_method_without_query_param(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            param = request.args.get("param", "default")
            return text(f"Received param: {param}")

    app.add_route(TestView.as_view(), "/query_test_default")

    request, response = app.test_client.get("/query_test_default")
    assert response.text == "Received param: default"