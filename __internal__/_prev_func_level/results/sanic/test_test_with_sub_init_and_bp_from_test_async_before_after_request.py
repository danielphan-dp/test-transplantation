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
            return text("Custom Status", status=201)

    app.add_route(DummyView.as_view(), "/custom-status")

    request, response = app.test_client.get("/custom-status")
    assert response.text == "Custom Status"
    assert response.status == 201

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"Param is {param}")

    app.add_route(DummyView.as_view(), "/query")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Param is test"

    request, response = app.test_client.get("/query")
    assert response.text == "Param is default"