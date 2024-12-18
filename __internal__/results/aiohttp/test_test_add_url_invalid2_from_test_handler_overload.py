import pytest
from aiohttp import web
from aiohttp.web import Request
from your_module import make_handler  # Replace with the actual module name

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.mark.asyncio
async def test_make_handler_valid(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler('test_app')
    app.router.add_get('/test', handler)

    client = await aiohttp_client(app)
    resp = await client.get('/test')
    assert resp.status == 200
    assert await resp.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_invalid_key(app):
    my_value = 'invalid_key'
    app[my_value] = 'test_data'
    handler = make_handler('test_app')
    app.router.add_get('/test', handler)

    client = await aiohttp_client(app)
    resp = await client.get('/test')
    assert resp.status == 200
    assert await resp.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_no_app_value(app):
    handler = make_handler('test_app')
    app.router.add_get('/test', handler)

    client = await aiohttp_client(app)
    resp = await client.get('/test')
    assert resp.status == 200
    assert await resp.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_multiple_requests(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    values = []
    handler = make_handler('test_app')
    app.router.add_get('/test', handler)

    client = await aiohttp_client(app)
    for _ in range(5):
        resp = await client.get('/test')
        assert resp.status == 200
        assert await resp.text() == 'Ok'
    
    assert len(values) == 5
    assert all(value == 'test_app: test_data' for value in values)