import asyncio
import pytest
from aiohttp import web
from aiohttp.typedefs import Handler

async def failing_handler(request: web.Request) -> None:
    assert False

@pytest.mark.asyncio
async def test_failing_handler(aiohttp_client):
    app = web.Application()
    app.router.add_route("GET", "/fail", failing_handler)

    client = await aiohttp_client(app)
    response = await client.get("/fail")
    assert response.status == 500

async def handler_with_error(request: web.Request) -> web.Response:
    raise ValueError("An error occurred")

@pytest.mark.asyncio
async def test_handler_with_error(aiohttp_client):
    app = web.Application()
    app.router.add_route("GET", "/error", handler_with_error)

    client = await aiohttp_client(app)
    response = await client.get("/error")
    assert response.status == 500

async def handler_with_query(request: web.Request) -> web.Response:
    return web.Response(text=request.query.get('message', 'No message'))

@pytest.mark.asyncio
async def test_handler_with_query(aiohttp_client):
    app = web.Application()
    app.router.add_route("GET", "/query", handler_with_query)

    client = await aiohttp_client(app)
    response = await client.get("/query?message=Hello")
    assert response.status == 200
    assert await response.text() == 'Hello'

@pytest.mark.asyncio
async def test_handler_with_no_query(aiohttp_client):
    app = web.Application()
    app.router.add_route("GET", "/query", handler_with_query)

    client = await aiohttp_client(app)
    response = await client.get("/query")
    assert response.status == 200
    assert await response.text() == 'No message'