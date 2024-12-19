import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"X-Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("X-Custom-Header") is None  # No custom header in response

def test_get_method_empty_response(app):
    @app.get("/empty")
    def empty_response(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""
    assert response.status == 200