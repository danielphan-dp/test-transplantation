import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method(aiohttp_client: AiohttpClient) -> None:
    """Test the close method of the aiohttp client."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    response = await client.get("/")
    assert response.status == 200
    await client.close()

    # Ensure that the client is closed properly
    with pytest.raises(RuntimeError):
        await client.get("/")  # This should raise an error since the client is closed

@pytest.mark.asyncio
async def test_close_multiple_times(aiohttp_client: AiohttpClient) -> None:
    """Test closing the client multiple times."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    await client.close()
    await client.close()  # Closing again should not raise an error

@pytest.mark.asyncio
async def test_close_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test closing the client while there are active requests."""
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(1)  # Simulate a long request
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    task = asyncio.create_task(client.get("/"))
    await asyncio.sleep(0.1)  # Allow the request to start
    await client.close()  # Close the client while the request is still active

    # Ensure that the task is still running
    assert not task.done()  # The task should not be done yet

    # Clean up
    await asyncio.sleep(1)  # Wait for the request to finish
    assert task.done()  # Now the task should be done after the sleep