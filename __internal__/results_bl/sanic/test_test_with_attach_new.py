import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    DummyView.attach(app, "/")
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_empty_request(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    DummyView.attach(app, "/")
    request, response = app.test_client.get("/", headers={})
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    DummyView.attach(app, "/")
    request, response = app.test_client.get("/?param=value")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_custom_header(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    DummyView.attach(app, "/")
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.text == "I am get method"