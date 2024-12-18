import asyncio
import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

@pytest.fixture
def app():
    return web.Application()

@pytest.fixture
def client(loop, app):
    async def make_client():
        return TestClient(TestServer(app))

    client = loop.run_until_complete(make_client())
    loop.run_until_complete(client.start_server())
    yield client
    loop.run_until_complete(client.close())

def test_client_close(client):
    assert not client.closed
    client.close()
    assert client.closed

def test_client_close_multiple_times(client):
    client.close()
    client.close()  # Closing again should not raise an error
    assert client.closed

def test_client_close_with_active_requests(client):
    async def handler(request):
        return web.Response(text="Hello, world")

    app.router.add_route('GET', '/', handler)
    
    async def make_request():
        await client.get('/')
    
    loop.run_until_complete(make_request())
    client.close()
    assert client.closed

def test_client_close_after_request(client):
    async def handler(request):
        return web.Response(text="Hello, world")

    app.router.add_route('GET', '/', handler)
    
    response = loop.run_until_complete(client.get('/'))
    assert response.status == 200
    client.close()
    assert client.closed

def test_client_close_with_error_handling(client):
    async def handler(request):
        raise web.HTTPInternalServerError()

    app.router.add_route('GET', '/', handler)
    
    with pytest.raises(web.HTTPInternalServerError):
        loop.run_until_complete(client.get('/'))
    client.close()
    assert client.closed