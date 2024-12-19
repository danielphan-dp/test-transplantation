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
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def get_with_params(request):
        name = request.args.get('name', 'World')
        return text(f'Hello, {name}!')

    request, response = app.test_client.get("/get_with_params?name=Test")
    assert response.status == 200
    assert response.text == "Hello, Test!"
    
    request, response = app.test_client.get("/get_with_params")
    assert response.status == 200
    assert response.text == "Hello, World!"