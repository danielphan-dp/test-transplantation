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

    client = await web.TestClient(app)
    resp = await client.get('/test')
    assert resp.status == 200
    text = await resp.text()
    assert text == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_invalid(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler('test_app')
    app.router.add_get('/test', handler)

    client = await web.TestClient(app)
    resp = await client.get('/invalid_route')
    assert resp.status == 404

@pytest.mark.asyncio
async def test_make_handler_with_different_appname(app):
    my_value = 'test_value'
    app[my_value] = 'another_test_data'
    handler = make_handler('another_app')
    app.router.add_get('/another_test', handler)

    client = await web.TestClient(app)
    resp = await client.get('/another_test')
    assert resp.status == 200
    text = await resp.text()
    assert text == 'Ok'