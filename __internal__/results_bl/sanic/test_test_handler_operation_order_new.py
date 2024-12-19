from sanic import Sanic
from sanic.response import text, empty
from sanic.signals import Event
import pytest

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_empty_request(app):
    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={'Content-Length': '0'})
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_query_params(app):
    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_handler_operation_order_with_get(app: Sanic):
    operations = []

    @app.on_request
    async def on_request(_):
        nonlocal operations
        operations.append(1)

    @app.on_response
    async def on_response(*_):
        nonlocal operations
        operations.append(5)

    @app.get("/get")
    async def handler(_):
        nonlocal operations
        operations.append(3)
        return empty()

    @app.signal(Event.HTTP_HANDLER_BEFORE)
    async def handler_before(**_):
        nonlocal operations
        operations.append(2)

    @app.signal(Event.HTTP_HANDLER_AFTER)
    async def handler_after(**_):
        nonlocal operations
        operations.append(4)

    app.test_client.get("/get")
    assert operations == [1, 2, 3, 4, 5]