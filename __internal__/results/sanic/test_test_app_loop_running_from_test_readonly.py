import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_query_param(app):
    @app.get("/get_with_param")
    async def handler(request):
        name = request.args.get('name', 'guest')
        return text(f'I am get method with {name}')

    request, response = app.test_client.get("/get_with_param?name=test")
    assert response.status == 200
    assert response.text == 'I am get method with test'

def test_get_method_no_query_param(app):
    @app.get("/get_with_param")
    async def handler(request):
        name = request.args.get('name', 'guest')
        return text(f'I am get method with {name}')

    request, response = app.test_client.get("/get_with_param")
    assert response.status == 200
    assert response.text == 'I am get method with guest'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_app_loop_running(app):
    @app.get("/test")
    async def handler(request):
        assert isinstance(app.loop, asyncio.AbstractEventLoop)
        return text("pass")

    request, response = app.test_client.get("/test")
    assert response.text == "pass"