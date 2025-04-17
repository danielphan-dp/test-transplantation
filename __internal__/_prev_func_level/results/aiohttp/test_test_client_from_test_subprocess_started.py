import asyncio
import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

@pytest.fixture
def client(loop: asyncio.AbstractEventLoop, app: web.Application) -> TestClient:
    async def make_client() -> TestClient:
        return TestClient(TestServer(app))

    client = loop.run_until_complete(make_client())
    loop.run_until_complete(client.start_server())
    yield client
    loop.run_until_complete(client.close())

def test_client_close(client: TestClient) -> None:
    assert not client.closed
    client.close()
    assert client.closed

def test_client_double_close(client: TestClient) -> None:
    client.close()
    client.close()  # Should not raise an error
    assert client.closed

def test_client_close_with_active_requests(client: TestClient) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    client.app.router.add_get('/', handler)
    loop.run_until_complete(client.get('/'))
    client.close()
    assert client.closed

def test_client_close_after_request(client: TestClient) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    client.app.router.add_get('/', handler)
    response = loop.run_until_complete(client.get('/'))
    assert response.status == 200
    client.close()
    assert client.closed

def test_client_close_without_start(client: TestClient) -> None:
    client.close()
    assert client.closed