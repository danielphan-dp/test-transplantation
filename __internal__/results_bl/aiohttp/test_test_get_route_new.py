import asyncio
import pytest
from aiohttp import web

async def test_get_route_not_found(loop: asyncio.AbstractEventLoop, test_client: _TestClient) -> None:
    resp = await test_client.request("GET", "/nonexistent")
    assert resp.status == 404

async def test_get_route_empty(loop: asyncio.AbstractEventLoop, test_client: _TestClient) -> None:
    resp = await test_client.request("GET", "/")
    text = await resp.text()
    assert text.strip() != ""

async def test_get_route_with_query(loop: asyncio.AbstractEventLoop, test_client: _TestClient) -> None:
    resp = await test_client.request("GET", "/?name=test")
    assert resp.status == 200
    text = await resp.text()
    assert "Hello, test" in text

async def test_get_route_invalid_method(loop: asyncio.AbstractEventLoop, test_client: _TestClient) -> None:
    resp = await test_client.request("POST", "/")
    assert resp.status == 405

@pytest.mark.asyncio
async def test_get_route(loop: asyncio.AbstractEventLoop, test_client: _TestClient) -> None:
    resp = await test_client.request("GET", "/")
    assert resp.status == 200
    text = await resp.text()
    assert _hello_world_str == text

loop.run_until_complete(test_get_route_not_found(loop, test_client))
loop.run_until_complete(test_get_route_empty(loop, test_client))
loop.run_until_complete(test_get_route_with_query(loop, test_client))
loop.run_until_complete(test_get_route_invalid_method(loop, test_client))