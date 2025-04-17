import asyncio
import pytest
from sanic import Sanic
from sanic_testing.testing import HOST
from conftest import get_port

@pytest.mark.asyncio
async def test_start_stop_app(app):
    finished = False

    async def handler(request):
        nonlocal finished
        await asyncio.sleep(3)
        finished = True
        return "Server is running"

    app.router.add_get("/", handler)

    async def run_test():
        await asyncio.sleep(1)
        async with app.test_client() as client:
            response = await client.get("/")
            assert response.status == 200
            assert await response.text == "Server is running"

    app.after_server_start(run_test)

    await start_stop_app(app)
    assert finished is True

@pytest.mark.asyncio
async def test_start_stop_app_with_keyboard_interrupt(app):
    finished = False

    async def handler(request):
        nonlocal finished
        await asyncio.sleep(3)
        finished = True
        return "Server is running"

    app.router.add_get("/", handler)

    async def run_test():
        await asyncio.sleep(1)
        async with app.test_client() as client:
            response = await client.get("/")
            assert response.status == 200
            assert await response.text == "Server is running"

    app.after_server_start(run_test)

    with pytest.raises(KeyboardInterrupt):
        await start_stop_app(app)  # Simulate KeyboardInterrupt

    assert finished is False  # Ensure the handler did not finish
    await asyncio.sleep(1.5)  # Allow time for shutdown
    assert finished is True  # Ensure the handler completes after shutdown