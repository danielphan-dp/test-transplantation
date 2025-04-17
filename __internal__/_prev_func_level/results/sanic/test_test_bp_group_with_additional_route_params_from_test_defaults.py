import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test_get")
    def get_method(request: Request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/test_get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/test_get", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # No custom header in response

def test_get_method_no_auth(app):
    request, response = app.test_client.get("/test_get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/test_get?param=value")
    assert response.text == "I am get method"
    assert response.status == 200