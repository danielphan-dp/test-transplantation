import random
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/greet")
    async def greet_handler(request):
        name = request.args.get('name', 'World')
        return text(f'Hello, {name}!')

    request, response = app.test_client.get("/greet?name=Alice")
    assert response.status == 200
    assert response.text == 'Hello, Alice!'

def test_get_method_with_empty_query_params(app):
    request, response = app.test_client.get("/greet")
    assert response.status == 200
    assert response.text == 'Hello, World!'