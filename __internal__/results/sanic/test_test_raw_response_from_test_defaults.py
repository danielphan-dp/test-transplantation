import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_test")
    def handler(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get_test")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get_test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure query params do not affect response

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get_test", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("X-Custom-Header") is None  # Ensure headers do not affect response

def test_get_method_empty_response(app):
    @app.get("/empty_response")
    def empty_handler(request):
        return text('')

    request, response = app.test_client.get("/empty_response")
    assert response.status == 200
    assert response.text == ''  # Test for empty response body