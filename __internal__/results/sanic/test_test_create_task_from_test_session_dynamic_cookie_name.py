import asyncio
import pytest
from threading import Event
from sanic.response import text

def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.body == b'I am get method'

def test_get_method_with_delay(app):
    e = Event()

    async def coro():
        await asyncio.sleep(0.05)
        e.set()

    app.add_task(coro)

    request, response = app.test_client.get("/get")
    assert response.body == b'I am get method'

    app.signal_router.reset()
    app.add_task(coro)
    await asyncio.sleep(0.1)
    request, response = app.test_client.get("/get")
    assert response.body == b'I am get method'