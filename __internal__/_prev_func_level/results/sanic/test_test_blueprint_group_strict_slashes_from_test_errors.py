import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    async def get_with_params(request):
        name = request.args.get('name', 'World')
        return text(f'I am get method, {name}')

    request, response = app.test_client.get("/get_with_params?name=Tester")
    assert response.status == 200
    assert response.text == 'I am get method, Tester'

def test_get_method_with_no_params(app):
    @app.get("/get_with_no_params")
    async def get_with_no_params(request):
        return text('I am get method, World')

    request, response = app.test_client.get("/get_with_no_params")
    assert response.status == 200
    assert response.text == 'I am get method, World'