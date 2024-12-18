import pytest
from aiohttp import web

async def failing_handler(request: web.Request) -> None:
    assert False

async def test_handler_asserts_false(aiohttp_client: web.Application) -> None:
    app = web.Application()
    app.router.add_get("/", failing_handler)
    client = await aiohttp_client(app)

    async with client.get("/") as resp:
        assert resp.status == 500

async def test_handler_returns_none(aiohttp_client: web.Application) -> None:
    async def handler(request: web.Request) -> None:
        return None

    app = web.Application()
    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    async with client.get("/") as resp:
        assert resp.status == 500

async def test_handler_returns_not_response(aiohttp_client: web.Application) -> None:
    async def handler(request: web.Request) -> str:
        return "abc"

    app = web.Application()
    app.router.add_get("/", handler)  # type: ignore[arg-type]
    client = await aiohttp_client(app)

    async with client.get("/") as resp:
        assert resp.status == 500

async def test_custom_expect_handler_plain(aiohttp_client: web.Application) -> None:
    async def custom_handler(request: web.Request) -> None:
        assert False

    app = web.Application()
    app.router.add_get("/", custom_handler)
    client = await aiohttp_client(app)

    async with client.get("/") as resp:
        assert resp.status == 500

async def test_custom_expect_handler_dynamic(aiohttp_client: web.Application) -> None:
    async def dynamic_handler(request: web.Request) -> None:
        assert False

    app = web.Application()
    app.router.add_get("/dynamic", dynamic_handler)
    client = await aiohttp_client(app)

    async with client.get("/dynamic") as resp:
        assert resp.status == 500