import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_async_loop(app):
    @app.get("/async-loop")
    async def handler(request):
        assert isinstance(app.loop, asyncio.AbstractEventLoop)
        return text("Async loop is running")

    request, response = app.test_client.get("/async-loop")
    assert response.text == "Async loop is running"

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    async def handler(request):
        name = request.args.get('name', 'Guest')
        return text(f'Hello, {name}')

    request, response = app.test_client.get("/get_with_params?name=John")
    assert response.text == 'Hello, John'

    request, response = app.test_client.get("/get_with_params")
    assert response.text == 'Hello, Guest'