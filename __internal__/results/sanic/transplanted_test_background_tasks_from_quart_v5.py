# Transplanted from tests/test_background_tasks.py to sanic/app.py

import asyncio
import time

import pytest
from sanic import Sanic
from sanic.response import text


@pytest.fixture
def app():
    app = Sanic("test_app")
    app.config.DATA = "data"
    return app


# Test to ensure a background task can be added and executed
async def test_background_task(app):
    data = None

    async def background():
        nonlocal data
        await asyncio.sleep(0.5)
        data = app.config.DATA

    @app.route("/")
    async def index(request):
        app.add_task(background)
        return text("")

    request, response = await app.asgi_client.get("/")
    assert response.status == 200

    # Allow some time for the background task to complete
    await asyncio.sleep(0.6)
    assert data == "data"


# Test to ensure a background task can be added during the lifespan of the app
async def test_lifespan_background_task(app):
    data = None

    async def background():
        nonlocal data
        await asyncio.sleep(0.5)
        data = app.config.DATA

    @app.main_process_start
    async def startup(app, loop):
        app.add_task(background)

    async with app.test_client() as client:
        pass

    assert data == "data"


# Test to ensure a synchronous background task can be added and executed
async def test_sync_background_task(app):
    data = None

    def background():
        nonlocal data
        time.sleep(0.5)
        data = app.config.DATA

    @app.route("/")
    async def index(request):
        app.add_task(background)
        return text("")

    request, response = await app.asgi_client.get("/")
    assert response.status == 200

    # Allow some time for the background task to complete
    await asyncio.sleep(0.6)
    assert data == "data"