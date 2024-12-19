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
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def get_with_params(request):
        name = request.args.get('name', 'Guest')
        return text(f'I am get method, {name}')

    request, response = app.test_client.get("/get_with_params?name=John")
    assert response.status == 200
    assert response.text == "I am get method, John"

def test_get_method_empty_query_params(app):
    request, response = app.test_client.get("/get_with_params")
    assert response.status == 200
    assert response.text == "I am get method, Guest"