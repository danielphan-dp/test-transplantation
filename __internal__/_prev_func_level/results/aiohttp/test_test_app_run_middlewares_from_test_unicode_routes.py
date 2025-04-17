import pytest
from aiohttp import web

async def failing_handler(request: web.Request) -> None:
    assert False

@pytest.mark.asyncio
async def test_handler_asserts_false() -> None:
    app = web.Application()
    app.router.add_get("/", failing_handler)
    
    client = await aiohttp_client(app)
    
    async with client.get("/") as resp:
        assert resp.status == 500

async def handler_with_no_return(request: web.Request) -> None:
    return None

@pytest.mark.asyncio
async def test_handler_returns_none() -> None:
    app = web.Application()
    app.router.add_get("/", handler_with_no_return)
    
    client = await aiohttp_client(app)
    
    async with client.get("/") as resp:
        assert resp.status == 500

async def handler_with_invalid_return(request: web.Request) -> str:
    return "Invalid return type"

@pytest.mark.asyncio
async def test_handler_returns_invalid_type() -> None:
    app = web.Application()
    app.router.add_get("/", handler_with_invalid_return)
    
    client = await aiohttp_client(app)
    
    async with client.get("/") as resp:
        assert resp.status == 500