import asyncio
import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

@pytest.fixture
def client(loop, app):
    async def make_client():
        return TestClient(TestServer(app))

    client = loop.run_until_complete(make_client())
    loop.run_until_complete(client.start_server())
    yield client
    loop.run_until_complete(client.close())

def test_client_close(client):
    assert client.is_running is True
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.close())
    assert client.is_running is False

def test_client_close_multiple_times(client):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.close())
    with pytest.raises(RuntimeError):
        loop.run_until_complete(client.close())

def test_client_close_with_active_requests(client):
    async def make_request():
        return await client.get('/')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_request())
    loop.run_until_complete(client.close())
    assert client.is_running is False

def test_client_close_without_start(client):
    new_client = TestClient(TestServer(web.Application()))
    with pytest.raises(RuntimeError):
        loop.run_until_complete(new_client.close())