import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")

    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")

    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get")
    async def get_handler(request):
        name = request.args.get('name', 'Guest')
        return text(f'I am get method, {name}')

    request, response = app.test_client.get("/get?name=John")

    assert response.text == 'I am get method, John'

def test_get_method_without_query_params(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method, Guest')

    request, response = app.test_client.get("/get")

    assert response.text == 'I am get method, Guest'