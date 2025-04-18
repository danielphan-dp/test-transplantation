# This test file was generated from tests/test_background_tasks.py to test the functionality in sanic/app.py through test transplantation.

import asyncio
import time
import pytest
from sanic import Sanic
from sanic.request import Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    app.config.DATA = "data"
    return app

# Test to ensure that a background task can be added and executed
@pytest.mark.asyncio
async def test_background_task(app: Sanic):
    data = None

    async def background():
        nonlocal data
        await asyncio.sleep(0.5)
        data = app.config.DATA

    @app.route("/")
    async def index(request: Request):
        app.add_task(background)
        return text("")

    request, response = await app.asgi_client.get("/")
    assert response.status == 200
    assert data == "data"

# Test to ensure that a background task can be added during the lifespan of the app
@pytest.mark.asyncio
async def test_lifespan_background_task(app: Sanic):
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

# Test to ensure that a synchronous background task can be added and executed
@pytest.mark.asyncio
async def test_sync_background_task(app: Sanic):
    data = None

    def background():
        nonlocal data
        time.sleep(0.5)
        data = app.config.DATA

    @app.route("/")
    async def index(request: Request):
        app.add_task(background)
        return text("")

    request, response = await app.asgi_client.get("/")
    assert response.status == 200
    assert data == "data"