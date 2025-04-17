import asyncio
import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_logging(app, caplog):
    @app.get("/")
    async def handler(request):
        return text('I am get method')

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert ("sanic.access", 20, "") in caplog.record_tuples

def test_get_method_with_query_param(app):
    @app.get("/greet")
    async def handler(request):
        name = request.args.get('name', 'World')
        return text(f'Hello, {name}!')

    request, response = app.test_client.get("/greet?name=Alice")
    assert response.status == 200
    assert response.text == "Hello, Alice!"

def test_get_method_without_query_param(app):
    @app.get("/greet")
    async def handler(request):
        name = request.args.get('name', 'World')
        return text(f'Hello, {name}!')

    request, response = app.test_client.get("/greet")
    assert response.status == 200
    assert response.text == "Hello, World!"