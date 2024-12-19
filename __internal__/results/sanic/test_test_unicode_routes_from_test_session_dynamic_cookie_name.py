import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"

def test_get_method_unicode(app):
    request, response = app.test_client.get("/你好")
    assert response.status == 404  # Expecting 404 since the route is not defined

def test_get_method_with_query_param(app):
    request, response = app.test_client.get("/test?param=value")
    assert response.text == "I am get method"  # Ensure query params do not affect response

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404  # Check for 404 on invalid route

def test_get_method_empty_route(app):
    request, response = app.test_client.get("/")
    assert response.status == 404  # Check for 404 on root if not defined