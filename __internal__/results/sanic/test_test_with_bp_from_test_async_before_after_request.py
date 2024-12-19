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

    app.add_route(DummyView.as_view(), "/get")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"Received param: {param}")

    app.add_route(DummyView.as_view(), "/get_with_param")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Received param: test"

    request, response = app.test_client.get("/get_with_param")
    assert response.text == "Received param: default"