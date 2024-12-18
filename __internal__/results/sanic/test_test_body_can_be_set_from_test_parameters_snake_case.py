import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test-get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test-get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/test-get?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/test-get", headers=headers)
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # No custom header in response

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/test-get", data={})
    assert response.text == "I am get method"
    assert response.status == 200