import pytest
from aiohttp import web
from aiohttp.test_utils import AiohttpClient

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.mark.parametrize("method", [
    "PROPFIND", "PROPPATCH", "COPY", "LOCK", "UNLOCK", "MOVE", "SUBSCRIBE", "UNSUBSCRIBE", "NOTIFY"
])
async def test_uncommon_http_methods(app, method, aiohttp_client):
    my_value = 'my_value'
    app[my_value] = 'test_value'
    handler = make_handler("test_app")
    app.router.add_route(method, "/handler/to/path", handler)
    
    client = await aiohttp_client(app)
    request = await client.request(method, "/handler/to/path")
    
    assert request.status == 200
    assert (await request.text()) == 'Ok'
    assert f'test_app: test_value' in values

async def test_handler_with_invalid_method(app, aiohttp_client):
    handler = make_handler("test_app")
    app.router.add_route("INVALID_METHOD", "/handler/to/path", handler)
    
    client = await aiohttp_client(app)
    request = await client.request("INVALID_METHOD", "/handler/to/path")
    
    assert request.status == 405  # Method Not Allowed

async def test_handler_with_no_app_value(app, aiohttp_client):
    my_value = 'my_value'
    handler = make_handler("test_app")
    app.router.add_route("GET", "/handler/to/path", handler)
    
    client = await aiohttp_client(app)
    request = await client.get("/handler/to/path")
    
    assert request.status == 200
    assert (await request.text()) == 'Ok'
    assert f'test_app: None' in values  # No value set in app

async def test_handler_multiple_requests(app, aiohttp_client):
    my_value = 'my_value'
    app[my_value] = 'test_value'
    handler = make_handler("test_app")
    app.router.add_route("GET", "/handler/to/path", handler)
    
    client = await aiohttp_client(app)
    
    for _ in range(5):
        request = await client.get("/handler/to/path")
        assert request.status == 200
        assert (await request.text()) == 'Ok'
    
    assert values == [f'test_app: test_value'] * 5  # Check if handler was called multiple times