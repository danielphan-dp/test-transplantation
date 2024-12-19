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

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_unicode(app):
    request, response = app.test_client.get("/get/你好")
    assert response.status == 404  # Expecting 404 since the route does not exist

def test_get_method_with_query_param(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'  # Ensure query params do not affect the response

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404  # Ensure invalid route returns 404

def test_get_method_empty_route(app):
    request, response = app.test_client.get("/")
    assert response.status == 404  # Ensure root route is not defined and returns 404