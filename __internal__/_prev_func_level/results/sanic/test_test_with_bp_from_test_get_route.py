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
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"I received {param}")

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.get("/?param=test")
    assert response.status == 200
    assert response.text == "I received test"

def test_get_method_with_empty_query_param(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"I received {param}")

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.get("/?param=")
    assert response.status == 200
    assert response.text == "I received "