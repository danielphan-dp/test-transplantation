import pytest
from sanic.app import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/test_get")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    @app.get("/test_get")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/non_existent_route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test_get")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/test_get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'