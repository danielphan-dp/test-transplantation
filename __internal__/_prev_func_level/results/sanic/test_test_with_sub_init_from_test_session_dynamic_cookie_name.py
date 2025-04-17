import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")
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
            return text("Empty request received")

    request, response = app.test_client.get("/empty")
    assert response.text == "Empty request received"

def test_get_method_with_query_param(app):
    class DummyView(HTTPMethodView, attach=app, uri="/query"):
        def get(self, request):
            param = request.args.get("param", "default")
            return text(f"Query param is {param}")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param is test"

def test_get_method_with_nonexistent_route(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_invalid_method(app):
    class DummyView(HTTPMethodView, attach=app, uri="/"):
        def get(self, request):
            return text("I am get method")

    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text