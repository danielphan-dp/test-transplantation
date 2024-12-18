import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

async def failing_handler(request: web.Request) -> None:
    assert False

async def test_handler_fails(aiohttp_client: AiohttpClient) -> None:
    app = web.Application()
    app.router.add_get("/", failing_handler)

    client = await aiohttp_client(app)

    async with client.get("/") as resp:
        assert resp.status == 500

async def test_handler_returns_string(aiohttp_client: AiohttpClient) -> None:
    async def string_handler(request: web.Request) -> str:
        return "This should not be returned"

    app = web.Application()
    app.router.add_get("/", string_handler)

    client = await aiohttp_client(app)

    async with client.get("/") as resp:
        assert resp.status == 500

async def test_handler_returns_none(aiohttp_client: AiohttpClient) -> None:
    async def none_handler(request: web.Request) -> None:
        return None

    app = web.Application()
    app.router.add_get("/", none_handler)

    client = await aiohttp_client(app)

    async with client.get("/") as resp:
        assert resp.status == 500

async def test_handler_with_invalid_response(aiohttp_client: AiohttpClient) -> None:
    async def invalid_response_handler(request: web.Request) -> int:
        return 42

    app = web.Application()
    app.router.add_get("/", invalid_response_handler)

    client = await aiohttp_client(app)

    async with client.get("/") as resp:
        assert resp.status == 500