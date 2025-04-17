import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")
    return app

def test_get_method(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # No change in response for query params

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"  # No change in response for headers

def test_get_method_empty_response(app):
    class EmptyView:
        def get(self, request):
            return text("")

    app.add_route(EmptyView().get, "/empty")
    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""  # Testing empty response case