import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method_on_open_connector(aiohttp_client: AiohttpClient) -> None:
    """Test the close method on an open connector."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Simulate opening a connection
    await client.get("/")
    
    # Close the client and check if it is closed
    await client.close()
    assert client.closed

@pytest.mark.asyncio
async def test_close_method_on_already_closed_connector(aiohttp_client: AiohttpClient) -> None:
    """Test the close method on an already closed connector."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Close the client
    await client.close()
    
    # Attempt to close again and check for no errors
    await client.close()
    assert client.closed

@pytest.mark.asyncio
async def test_close_method_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test the close method while there are active requests."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(1)  # Simulate long request
        return web.Response(text="Done")

    app.router.add_route("GET", "/", handler)

    # Start a request
    task = asyncio.create_task(client.get("/"))
    
    # Close the client while the request is still active
    await client.close()
    
    # Ensure the task is still running
    assert not task.done()

@pytest.mark.asyncio
async def test_close_method_with_no_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test the close method when there are no active requests."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Close the client with no active requests
    await client.close()
    assert client.closed

@pytest.mark.asyncio
async def test_close_method_multiple_times(aiohttp_client: AiohttpClient) -> None:
    """Test calling close method multiple times."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Close the client multiple times
    await client.close()
    await client.close()
    await client.close()
    
    assert client.closed