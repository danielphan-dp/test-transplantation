import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.get("/")

    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            my_param = request.args.get('param', 'default')
            return text(f"I am get method with {my_param}")

    app.add_route(DummyView.as_view(), "/")

    request, response = app.test_client.get("/?param=test_param")

    assert response.status == 200
    assert response.text == "I am get method with test_param"

def test_get_method_with_invalid_route(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView.as_view(), "/valid")

    request, response = app.test_client.get("/invalid")

    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_empty_response(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("")

    app.add_route(DummyView.as_view(), "/empty")

    request, response = app.test_client.get("/empty")

    assert response.status == 200
    assert response.text == ""