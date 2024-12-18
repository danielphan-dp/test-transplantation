import asyncio
import pytest
from aiohttp import web
from aiohttp.test_utils import _TestClient

_hello_world_str = "Hello, World!"

async def test_get_route_with_different_methods(loop: asyncio.AbstractEventLoop, test_client: _TestClient) -> None:
    methods = ['GET', 'HEAD']
    for method in methods:
        resp = await test_client.request(method, '/')
        assert resp.status == 200
        text = await resp.text()
        assert _hello_world_str == text

loop.run_until_complete(test_get_route_with_different_methods(loop, test_client))

async def test_get_route_with_invalid_path(loop: asyncio.AbstractEventLoop, test_client: _TestClient) -> None:
    resp = await test_client.request('GET', '/invalid')
    assert resp.status == 404

loop.run_until_complete(test_get_route_with_invalid_path(loop, test_client))

async def test_get_route_with_query_params(loop: asyncio.AbstractEventLoop, test_client: _TestClient) -> None:
    resp = await test_client.request('GET', '/?param=value')
    assert resp.status == 200
    text = await resp.text()
    assert _hello_world_str == text

loop.run_until_complete(test_get_route_with_query_params(loop, test_client))