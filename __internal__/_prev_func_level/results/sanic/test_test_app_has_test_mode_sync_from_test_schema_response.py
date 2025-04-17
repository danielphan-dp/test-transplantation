import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def handler(request):
        name = request.args.get('name', 'Guest')
        return text(f'Hello, {name}')

    request, response = app.test_client.get("/get_with_params?name=John")
    assert response.status == 200
    assert response.text == 'Hello, John'

def test_get_method_without_query_params(app):
    @app.get("/get_with_params")
    def handler(request):
        name = request.args.get('name', 'Guest')
        return text(f'Hello, {name}')

    request, response = app.test_client.get("/get_with_params")
    assert response.status == 200
    assert response.text == 'Hello, Guest'