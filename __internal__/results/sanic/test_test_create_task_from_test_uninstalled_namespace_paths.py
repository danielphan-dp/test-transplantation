import os
import pytest
from sanic.response import text
from asyncio import Event

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

def test_reset_environment_variable(app):
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_create_task_with_reset(app):
    e = Event()

    async def coro():
        await asyncio.sleep(0.05)
        e.set()

    @app.route("/early")
    def not_set(request):
        return text(str(e.is_set()))

    @app.route("/late")
    async def set(request):
        await asyncio.sleep(0.1)
        return text(str(e.is_set()))

    app.add_task(coro)

    request, response = app.test_client.get("/early")
    assert response.body == b"False"

    app.signal_router.reset()
    app.add_task(coro)
    request, response = app.test_client.get("/late")
    assert response.body == b"True"

def test_create_task_with_no_environment_variable(app):
    e = Event()

    async def coro():
        await asyncio.sleep(0.05)
        e.set()

    @app.route("/check")
    async def check(request):
        return text(str(e.is_set()))

    app.add_task(coro)

    request, response = app.test_client.get("/check")
    assert response.body == b"False"

    app.signal_router.reset()
    app.add_task(coro)
    await asyncio.sleep(0.1)
    request, response = app.test_client.get("/check")
    assert response.body == b"True"