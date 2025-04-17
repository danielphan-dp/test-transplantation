import pytest
from aiohttp import web
from aiohttp.web import Request
from aiohttp.test_utils import AiohttpClient

@pytest.mark.parametrize('appname, my_value', [
    ('test_app', 'test_value'),
    ('another_app', 'another_value'),
])
async def test_make_handler(aiohttp_client: AiohttpClient, appname: str, my_value: str) -> None:
    values = []
    
    async def handler(request: Request) -> web.Response:
        values.append(f'{appname}: {request.app[my_value]}')
        return web.Response(text='Ok')

    app = web.Application()
    app[my_value] = 'value_data'
    app.router.add_get("/", handler)

    client = await aiohttp_client(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert values == [f'{appname}: value_data']

@pytest.mark.parametrize('appname, my_value', [
    ('test_app', 'non_existent_value'),
])
async def test_make_handler_non_existent_value(aiohttp_client: AiohttpClient, appname: str, my_value: str) -> None:
    values = []
    
    async def handler(request: Request) -> web.Response:
        values.append(f'{appname}: {request.app[my_value]}')
        return web.Response(text='Ok')

    app = web.Application()
    app.router.add_get("/", handler)

    client = await aiohttp_client(app)

    resp = await client.get("/")
    assert resp.status == 500  # Expecting an error due to non-existent value
    assert not values  # No values should be appended due to the error

@pytest.mark.parametrize('appname', [
    ('invalid_app_name'),
])
async def test_make_handler_invalid_appname(aiohttp_client: AiohttpClient, appname: str) -> None:
    values = []
    
    async def handler(request: Request) -> web.Response:
        values.append(f'{appname}: {request.app["my_value"]}')
        return web.Response(text='Ok')

    app = web.Application()
    app['my_value'] = 'value_data'
    app.router.add_get("/", handler)

    client = await aiohttp_client(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert values == [f'{appname}: value_data']