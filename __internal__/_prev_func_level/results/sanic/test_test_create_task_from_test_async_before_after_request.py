import asyncio
import pytest
from threading import Event
from sanic.response import text

def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')

    request, response = app.test_client.get('/get')
    assert response.body == b'I am get method'

def test_get_method_with_delay(app):
    e = Event()

    async def coro():
        await asyncio.sleep(0.1)
        e.set()

    app.add_task(coro)

    request, response = app.test_client.get('/get')
    assert response.body == b'I am get method'
    assert e.is_set() is False

    await asyncio.sleep(0.1)
    assert e.is_set() is True

def test_get_method_invalid_route(app):
    request, response = app.test_client.get('/invalid')
    assert response.status == 404
    assert b'Requested URL /invalid not found' in response.body

def test_get_method_with_query_param(app):
    class DummyView:
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'Param is {param}')

    app.add_route(DummyView().get, '/get_with_param')

    request, response = app.test_client.get('/get_with_param?param=test')
    assert response.body == b'Param is test'

    request, response = app.test_client.get('/get_with_param')
    assert response.body == b'Param is default'