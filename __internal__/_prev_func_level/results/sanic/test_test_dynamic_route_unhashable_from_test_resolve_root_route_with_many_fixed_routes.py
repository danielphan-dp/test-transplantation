import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test")
    def get_method(request):
        return text(f'I am get method with query {request.args}')

    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method with query {"param": ["value"]}'

def test_get_method_with_empty_query_params(app):
    @app.get("/test")
    def get_method(request):
        return text(f'I am get method with query {request.args}')

    request, response = app.test_client.get("/test?")
    assert response.status == 200
    assert response.text == 'I am get method with query {}'