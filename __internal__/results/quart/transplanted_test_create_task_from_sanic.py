# Transplanted from tests/test_create_task.py to src/quart/asgi.py

import asyncio
from threading import Event

import pytest
from quart import Quart, websocket
from quart.wrappers import Response

from src.quart.asgi import ASGIHTTPConnection, ASGIWebsocketConnection, ASGILifespan


@pytest.fixture
def app():
    app = Quart(__name__)
    return app


def test_asgi_http_connection(app):
    e = Event()

    async def coro():
        await asyncio.sleep(0.05)
        e.set()

    @app.route("/early")
    async def not_set():
        return Response(str(e.is_set()))

    @app.route("/late")
    async def set():
        await asyncio.sleep(0.1)
        return Response(str(e.is_set()))

    app.add_background_task(coro)

    test_client = app.test_client()
    response = test_client.get("/early")
    assert response.data == b"False"

    app.add_background_task(coro)
    response = test_client.get("/late")
    assert response.data == b"True"


def test_asgi_websocket_connection(app):
    e = Event()

    async def coro():
        e.set()

    @app.websocket("/ws")
    async def ws():
        await websocket.accept()
        await websocket.send(str(e.is_set()))

    @app.before_serving
    async def setup():
        app.add_background_task(coro)

    test_client = app.test_client()
    with test_client.websocket("/ws") as ws:
        response = ws.receive()
        assert response == "True"


def test_asgi_lifespan(app):
    e = Event()

    async def coro():
        e.set()

    @app.before_serving
    async def setup():
        app.add_background_task(coro)

    @app.route("/")
    async def index():
        return Response(str(e.is_set()))

    test_client = app.test_client()
    response = test_client.get("/")
    assert response.data == b"True"


def test_create_named_task_fails_outside_app(app):
    async def dummy(): ...

    message = "Cannot name task outside of a running application"
    with pytest.raises(RuntimeError, match=message):
        app.add_background_task(dummy, name="dummy_task")
    assert not app._task_registry

    message = 'Registered task named "dummy_task" not found.'
    with pytest.raises(KeyError, match=message):
        app.get_task("dummy_task")