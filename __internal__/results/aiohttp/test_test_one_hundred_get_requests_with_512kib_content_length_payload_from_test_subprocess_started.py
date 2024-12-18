import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method_on_open_connection(aiohttp_client: AiohttpClient) -> None:
    """Test the close method on an open connection."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Simulate opening a connection
    await client.get("/")
    
    # Close the client and assert that it is closed
    await client.close()
    assert client.closed

@pytest.mark.asyncio
async def test_close_method_on_already_closed_connection(aiohttp_client: AiohttpClient) -> None:
    """Test the close method on an already closed connection."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Close the client
    await client.close()
    
    # Attempt to close again and ensure no errors are raised
    await client.close()
    assert client.closed

@pytest.mark.asyncio
async def test_close_method_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test the close method while there are active requests."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(1)  # Simulate a long request
        return web.Response(text="Hello, world")

    app.router.add_route("GET", "/", handler)

    # Start a request
    task = asyncio.create_task(client.get("/"))
    
    # Close the client while the request is still active
    await client.close()
    
    # Ensure the task is still running
    assert not task.done()

@pytest.mark.asyncio
async def test_close_method_with_multiple_requests(aiohttp_client: AiohttpClient) -> None:
    """Test the close method after multiple requests."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app.router.add_route("GET", "/", handler)

    # Send multiple requests
    tasks = [client.get("/") for _ in range(10)]
    responses = await asyncio.gather(*tasks)
    
    # Close the client
    await client.close()
    
    # Ensure all responses were read
    for response in responses:
        await response.read()
    
    assert client.closed