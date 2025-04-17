import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method(aiohttp_client: AiohttpClient) -> None:
    """Test the close method of the connector."""
    
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")
    
    app.router.add_route("GET", "/", handler)
    
    client = await aiohttp_client(app)
    
    # Simulate opening and closing the client
    await client.get("/")
    await client.close()
    
    # Check if the client is closed
    assert client.closed is True

@pytest.mark.asyncio
async def test_close_method_multiple_calls(aiohttp_client: AiohttpClient) -> None:
    """Test multiple calls to close method."""
    
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")
    
    app.router.add_route("GET", "/", handler)
    
    client = await aiohttp_client(app)
    
    await client.get("/")
    await client.close()
    
    # Call close again and ensure no errors occur
    await client.close()
    assert client.closed is True

@pytest.mark.asyncio
async def test_close_method_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test close method while there are active requests."""
    
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(1)  # Simulate long request
        return web.Response(text="Hello, world")
    
    app.router.add_route("GET", "/", handler)
    
    client = await aiohttp_client(app)
    
    # Start a request
    task = asyncio.create_task(client.get("/"))
    
    # Close the client while the request is still active
    await client.close()
    
    # Ensure the task is still running
    assert not task.done()  # The request should still be in progress

    # Clean up
    await asyncio.sleep(1)  # Wait for the request to finish
    assert client.closed is True