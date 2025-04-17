import pytest
from aiohttp import web
from aiohttp.web import Request
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_handler_returns_ok(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = web.Request(
        method='GET',
        path='/test',
        app=web.Application(),
        match_info={'path': '/test'}
    )
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_handler_with_appname(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test_app", handler)

    request = web.Request(
        method='GET',
        path='/test_app',
        app=web.Application(),
        match_info={'path': '/test_app'}
    )
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_handler_appname_value(router):
    appname = "test_app"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/test_value", handler)

    request = web.Request(
        method='GET',
        path='/test_value',
        app=web.Application(),
        match_info={'path': '/test_value'}
    )
    await handler(request)

    assert f'{appname}: {request.app[my_value]}' in values

@pytest.mark.asyncio
async def test_double_add_url_with_different_names(router):
    appname1 = "app_one"
    appname2 = "app_two"
    handler1 = make_handler(appname1)
    handler2 = make_handler(appname2)
    router.add_route("GET", "/get_one", handler1, name="name_one")

    with pytest.raises(ValueError) as ctx:
        router.add_route("GET", "/get_two", handler2, name="name_one")
    assert str(ctx.value).startswith("Duplicate 'name_one', already handled by")

@pytest.mark.asyncio
async def test_handler_returns_none(router):
    async def handler(request: Request) -> None:
        return None

    router.add_route("GET", "/none", handler)

    request = web.Request(
        method='GET',
        path='/none',
        app=web.Application(),
        match_info={'path': '/none'}
    )
    response = await handler(request)

    assert response is None