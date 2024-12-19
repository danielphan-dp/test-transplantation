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

def test_get_method_empty_response(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("")

    app.add_route(DummyView.as_view(), "/empty")

    request, response = app.test_client.get("/empty")

    assert response.text == ""

def test_get_method_with_custom_status(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("Custom status", status=201)

    app.add_route(DummyView.as_view(), "/custom_status")

    request, response = app.test_client.get("/custom_status")

    assert response.text == "Custom status"
    assert response.status == 201

def test_get_method_with_query_param(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            param = request.args.get("param", "default")
            return text(f"Received param: {param}")

    app.add_route(DummyView.as_view(), "/query")

    request, response = app.test_client.get("/query?param=test")

    assert response.text == "Received param: test"

def test_get_method_without_query_param(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            param = request.args.get("param", "default")
            return text(f"Received param: {param}")

    app.add_route(DummyView.as_view(), "/query")

    request, response = app.test_client.get("/query")

    assert response.text == "Received param: default"