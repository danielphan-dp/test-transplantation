import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_connector(aiohttp_client: AiohttpClient) -> None:
    """Test the close method of the connector."""
    
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Simulate opening and closing the connector
    await client.close()
    
    # Check if the connector is closed
    assert client.closed is True

@pytest.mark.asyncio
async def test_close_multiple_times(aiohttp_client: AiohttpClient) -> None:
    """Test closing the connector multiple times."""
    
    app = web.Application()
    client = await aiohttp_client(app)
    
    await client.close()
    
    # Closing again should not raise an error
    await client.close()
    assert client.closed is True

@pytest.mark.asyncio
async def test_close_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test closing the connector while there are active requests."""
    
    app = web.Application()
    message_count = 10

    async def handler(request: web.Request) -> web.Response:
        return web.Response()

    app.router.add_route("POST", "/", handler)
    client = await aiohttp_client(app)

    async def send_requests() -> None:
        for _ in range(message_count):
            await client.post("/", data=b"any")

    # Start sending requests
    task = asyncio.create_task(send_requests())
    
    # Close the client while requests are being sent
    await client.close()
    
    # Ensure the task is completed
    await task
    assert client.closed is True

@pytest.mark.asyncio
async def test_close_no_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test closing the connector with no active requests."""
    
    app = web.Application()
    client = await aiohttp_client(app)
    
    await client.close()
    assert client.closed is True

@pytest.mark.asyncio
async def test_close_after_error(aiohttp_client: AiohttpClient) -> None:
    """Test closing the connector after an error occurs."""
    
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Simulate an error
    with pytest.raises(Exception):
        raise Exception("Simulated error")
    
    await client.close()
    assert client.closed is True