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
    
    # Ensure the client is not closed initially
    assert not client.closed

    # Close the client
    await client.close()

    # Ensure the client is closed after calling close
    assert client.closed

    # Attempt to make a request after closing the client
    with pytest.raises(RuntimeError, match="Client session is closed"):
        await client.get("/")