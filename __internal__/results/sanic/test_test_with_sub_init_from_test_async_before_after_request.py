import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class DummyView(HTTPMethodView, attach=app, uri="/get"):
        def get(self, request):
            return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    class DummyView(HTTPMethodView, attach=app, uri="/get_with_param"):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Received param: test"

def test_get_method_without_query_param(app):
    class DummyView(HTTPMethodView, attach=app, uri="/get_with_param"):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param")
    assert response.text == "Received param: default"