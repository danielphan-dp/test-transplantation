import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method(aiohttp_client: AiohttpClient) -> None:
    """Test the close method of the aiohttp client."""
    
    app = web.Application()
    app.router.add_route("GET", "/", lambda request: web.Response(text="Hello, world"))

    client = await aiohttp_client(app)
    
    # Ensure the client is open before closing
    assert not client.closed

    # Close the client
    client.close()

    # Verify that the client is closed
    assert client.closed

    # Attempt to make a request after closing to ensure it raises an error
    with pytest.raises(RuntimeError, match="Client session is closed"):
        await client.get("/")