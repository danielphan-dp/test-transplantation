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
    resp = await client.get("/")
    assert resp.status == 200
    await client.close()

    # Ensure that the client is closed properly
    with pytest.raises(RuntimeError):
        await client.get("/")  # This should raise an error since the client is closed

@pytest.mark.asyncio
async def test_close_multiple_closes(aiohttp_client: AiohttpClient) -> None:
    """Test closing the client multiple times."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    await client.get("/")
    await client.close()
    
    # Close again and ensure no error is raised
    await client.close()  # Should not raise an error

@pytest.mark.asyncio
async def test_close_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test closing the client while there are active requests."""
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(1)  # Simulate a long request
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    
    # Start a request that will take time
    task = asyncio.create_task(client.get("/"))
    
    # Close the client while the request is still active
    await client.close()
    
    # Ensure the task is still running
    assert not task.done()  # The task should still be running

    # Clean up by waiting for the task to finish
    await task

@pytest.mark.asyncio
async def test_close_after_error(aiohttp_client: AiohttpClient) -> None:
    """Test closing the client after an error occurs."""
    
    async def handler(request: web.Request) -> web.Response:
        raise web.HTTPInternalServerError()

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    
    # Expect an error when making the request
    with pytest.raises(web.HTTPInternalServerError):
        await client.get("/")
    
    # Now close the client
    await client.close()  # Ensure this does not raise an error