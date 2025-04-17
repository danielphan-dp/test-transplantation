import pytest
from aiohttp import web
from aiohttp.web import Request, Response
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.mark.parametrize('appname', ['test_app', 'another_app'])
async def test_make_handler(appname):
    values = []
    app = web.Application()
    my_value = 'my_value'
    app[my_value] = 'some_value'

    handler = make_handler(appname)
    app.router.add_get('/', handler)

    client = await aiohttp_client(app)
    resp = await client.get('/')
    
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert values == [f'{appname}: some_value']

@pytest.mark.parametrize('appname', ['invalid name', 'class'])
async def test_make_handler_invalid_appname(appname):
    values = []
    app = web.Application()
    my_value = 'my_value'
    app[my_value] = 'some_value'

    handler = make_handler(appname)
    app.router.add_get('/', handler)

    client = await aiohttp_client(app)
    resp = await client.get('/')
    
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert values == [f'{appname}: some_value']