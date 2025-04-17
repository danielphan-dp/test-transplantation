import asyncio
import pytest
from threading import Event
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_delay(app):
    e = Event()

    async def coro():
        await asyncio.sleep(0.1)
        e.set()

    @app.before_server_start
    async def setup(app, _):
        app.add_task(coro, name="dummy_task")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert e.is_set() is True

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert b"Requested URL /invalid not found" in response.body

def test_get_method_with_query_param(app):
    @app.route("/get_with_param")
    async def get_with_param(request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Param is test"