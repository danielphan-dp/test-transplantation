import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/test_get")
    def get_method_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test_get")
    assert response.text == 'I am get method'

def test_get_method_empty_request(app):
    @app.get("/test_get_empty")
    def get_method_empty_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test_get_empty")
    assert response.text == 'I am get method'

def test_get_method_with_query_params(app):
    @app.get("/test_get_with_query")
    def get_method_query_handler(request):
        return text('I am get method with query')

    request, response = app.test_client.get("/test_get_with_query?param=value")
    assert response.text == 'I am get method with query'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404