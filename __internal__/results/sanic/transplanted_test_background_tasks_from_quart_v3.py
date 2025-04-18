# Transplanted from tests/test_background_tasks.py in Quart to sanic/app.py in Sanic

import asyncio
import time
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.asyncio
async def test_background_task():
    app = Sanic("test_background_task")
    app.config.DATA = "data"

    data = None

    async def background():
        nonlocal data
        await asyncio.sleep(0.5)
        data = app.config.DATA

    @app.route("/")
    async def index(request):
        app.add_task(background())
        return text("")

    request, response = await app.asgi_client.get("/")
    assert response.status == 200
    assert data == "data"

@pytest.mark.asyncio
async def test_lifespan_background_task():
    app = Sanic("test_lifespan_background_task")
    app.config.DATA = "data"

    data = None

    async def background():
        nonlocal data
        await asyncio.sleep(0.5)
        data = app.config.DATA

    @app.main_process_start
    async def startup(app, loop):
        app.add_task(background())

    async with app.asgi_client:
        pass

    assert data == "data"

@pytest.mark.asyncio
async def test_sync_background_task():
    app = Sanic("test_sync_background_task")
    app.config.DATA = "data"

    data = None

    def background():
        nonlocal data
        time.sleep(0.5)
        data = app.config.DATA

    @app.route("/")
    async def index(request):
        app.add_task(background())
        return text("")

    request, response = await app.asgi_client.get("/")
    assert response.status == 200
    assert data == "data"