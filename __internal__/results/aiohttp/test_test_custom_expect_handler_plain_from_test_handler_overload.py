import pytest
from aiohttp import web
from aiohttp.web import Request
from aiohttp.test_utils import AiohttpClient

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_with_valid_appname(router):
    appname = "test_app"
    my_value = "my_key"
    values = []
    
    async def handler(request: Request) -> web.Response:
        values.append(f'{appname}: {request.app[my_value]}')
        return web.Response(text='Ok')

    router.add_route("GET", "/", handler)
    app = web.Application()
    app[my_value] = "test_value"
    client = await AiohttpClient(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert values == [f'{appname}: test_value']

@pytest.mark.asyncio
async def test_make_handler_with_missing_key(router):
    appname = "test_app"
    my_value = "my_key"
    values = []
    
    async def handler(request: Request) -> web.Response:
        values.append(f'{appname}: {request.app[my_value]}')
        return web.Response(text='Ok')

    router.add_route("GET", "/", handler)
    app = web.Application()  # my_value is not set
    client = await AiohttpClient(app)

    resp = await client.get("/")
    assert resp.status == 500  # Expecting an error due to missing key

@pytest.mark.asyncio
async def test_make_handler_with_empty_appname(router):
    appname = ""
    my_value = "my_key"
    values = []
    
    async def handler(request: Request) -> web.Response:
        values.append(f'{appname}: {request.app[my_value]}')
        return web.Response(text='Ok')

    router.add_route("GET", "/", handler)
    app = web.Application()
    app[my_value] = "test_value"
    client = await AiohttpClient(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert values == [f'{appname}: test_value']

@pytest.mark.asyncio
async def test_make_handler_with_special_characters(router):
    appname = "test_app_!@#"
    my_value = "my_key"
    values = []
    
    async def handler(request: Request) -> web.Response:
        values.append(f'{appname}: {request.app[my_value]}')
        return web.Response(text='Ok')

    router.add_route("GET", "/", handler)
    app = web.Application()
    app[my_value] = "test_value"
    client = await AiohttpClient(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert values == [f'{appname}: test_value']