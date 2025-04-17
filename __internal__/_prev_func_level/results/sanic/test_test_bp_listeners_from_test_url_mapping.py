import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

class DummyView(HTTPMethodView):
    def get(self, request):
        return text('I am get method')

def test_get_method(app):
    app.add_route(DummyView.as_view(), "/")
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    app.add_route(DummyView.as_view(), "/")
    request, response = app.test_client.get("/?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_method(app):
    app.add_route(DummyView.as_view(), "/")
    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text

def test_get_method_with_headers(app):
    app.add_route(DummyView.as_view(), "/")
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # No custom header in response