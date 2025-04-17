import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

class TestConnectorClose:
    async def test_close_connector(self, loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
        """Test the close method of the connector."""
        app = web.Application()
        client = await aiohttp_client(app)
        
        # Simulate opening and closing the connector
        await client.close()
        
        # Check if the connector is closed
        assert client.closed

    async def test_close_multiple_times(self, loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
        """Test closing the connector multiple times."""
        app = web.Application()
        client = await aiohttp_client(app)
        
        await client.close()
        
        # Closing again should not raise an error
        await client.close()
        assert client.closed

    async def test_close_with_active_requests(self, loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
        """Test closing the connector while there are active requests."""
        app = web.Application()
        message_count = 10

        async def handler(request: web.Request) -> web.Response:
            return web.Response()

        app.router.add_route("GET", "/", handler)
        client = await aiohttp_client(app)

        async def make_requests():
            for _ in range(message_count):
                await client.get("/")

        # Run requests in the background
        task = loop.create_task(make_requests())
        
        # Close the client while requests are still being processed
        await client.close()
        
        # Ensure the task is completed
        await task
        assert client.closed

    async def test_close_with_error_handling(self, loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
        """Test closing the connector with error handling."""
        app = web.Application()
        client = await aiohttp_client(app)

        # Simulate an error during a request
        async def handler(request: web.Request) -> web.Response:
            raise Exception("Simulated error")

        app.router.add_route("GET", "/", handler)

        try:
            await client.get("/")
        except Exception:
            pass
        
        # Now close the client
        await client.close()
        assert client.closed