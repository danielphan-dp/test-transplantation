import pytest
from sanic import Sanic
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

    DummyView.attach(app, "/")

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_with_different_path(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("I am get method from a different path")

    DummyView.attach(app, "/different")

    request, response = app.test_client.get("/different")
    assert response.text == "I am get method from a different path"

def test_get_method_with_query_param(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text(f"Query param value: {request.args.get('param', 'not provided')}")

    DummyView.attach(app, "/query")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param value: test"

def test_get_method_with_no_query_param(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text(f"Query param value: {request.args.get('param', 'not provided')}")

    DummyView.attach(app, "/query")

    request, response = app.test_client.get("/query")
    assert response.text == "Query param value: not provided"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_method_not_allowed(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    DummyView.attach(app, "/")

    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text