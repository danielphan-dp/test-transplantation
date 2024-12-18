import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

class TestCloseMethod:
    @pytest.mark.asyncio
    async def test_close_method_not_closed(self, aiohttp_client):
        app = web.Application()
        client = await aiohttp_client(app)
        assert not client.closed
        client.close()
        assert client.closed

    @pytest.mark.asyncio
    async def test_close_method_multiple_calls(self, aiohttp_client):
        app = web.Application()
        client = await aiohttp_client(app)
        client.close()
        client.close()  # Calling close again should not raise an error
        assert client.closed

    @pytest.mark.asyncio
    async def test_close_method_with_active_requests(self, aiohttp_client):
        app = web.Application()
        message_count = 10

        async def handler(request: web.Request) -> web.Response:
            return web.Response()

        app.router.add_route("GET", "/", handler)
        client = await aiohttp_client(app)

        async def make_requests():
            for _ in range(message_count):
                await client.get("/")

        await asyncio.gather(make_requests())
        client.close()
        assert client.closed

    @pytest.mark.asyncio
    async def test_close_method_with_exception(self, aiohttp_client):
        app = web.Application()
        client = await aiohttp_client(app)

        with pytest.raises(Exception):
            raise Exception("Simulated exception before close")

        client.close()
        assert client.closed

    @pytest.mark.asyncio
    async def test_close_method_after_request(self, aiohttp_client):
        app = web.Application()
        async def handler(request: web.Request) -> web.Response:
            return web.Response()

        app.router.add_route("GET", "/", handler)
        client = await aiohttp_client(app)
        await client.get("/")
        client.close()
        assert client.closed