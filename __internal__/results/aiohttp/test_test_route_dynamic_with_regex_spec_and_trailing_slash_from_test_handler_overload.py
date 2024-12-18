import pytest
from aiohttp import web
from aiohttp.test_utils import AiohttpClient

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.fixture
def client(aiohttp_client, app):
    return aiohttp_client(app)

def make_handler(appname: str):
    values = []
    async def handler(request: web.Request) -> web.Response:
        values.append(f'{appname}: {request.app["my_value"]}')
        return web.Response(text='Ok')
    return handler

async def test_make_handler(client):
    appname = "test_app"
    handler = make_handler(appname)
    client.app.router.add_get('/test', handler)
    client.app['my_value'] = 'value123'
    
    resp = await client.get('/test')
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert handler.__closure__[0].cell_contents == [f'{appname}: value123']

async def test_make_handler_no_value(client):
    appname = "test_app"
    handler = make_handler(appname)
    client.app.router.add_get('/test', handler)
    
    resp = await client.get('/test')
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert handler.__closure__[0].cell_contents == [f'{appname}: None']  # No my_value set

async def test_make_handler_with_different_appname(client):
    appname = "another_app"
    handler = make_handler(appname)
    client.app.router.add_get('/test', handler)
    client.app['my_value'] = 'value456'
    
    resp = await client.get('/test')
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert handler.__closure__[0].cell_contents == [f'{appname}: value456']