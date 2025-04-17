import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")

    class DummyView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.as_view(), "/")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    request, response = app.test_client.get("/?param=test")
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_empty_request(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200