import asyncio
import pytest
from aiohttp import hdrs, web
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
        await client.get("/")  # Should raise an error since the client is closed

@pytest.mark.asyncio
async def test_close_multiple_times(aiohttp_client: AiohttpClient) -> None:
    """Test closing the client multiple times."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    await client.close()
    
    # Closing again should not raise an error
    await client.close()  # This should be a no-op

@pytest.mark.asyncio
async def test_close_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test closing the client while there are active requests."""
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(0.1)  # Simulate a long request
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    
    # Start a request that will take some time
    task = asyncio.create_task(client.get("/"))
    
    # Close the client while the request is still active
    await client.close()
    
    # Ensure that the task is cancelled
    with pytest.raises(asyncio.CancelledError):
        await task  # This should raise an error since the request was cancelled