import pytest
from aiohttp import web
from aiohttp.web import Request, Response
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_returns_ok_response(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await router["/test"].get()
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_inserts_appname_into_values(router):
    appname = "test_app"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = web.Request(
        method='GET',
        path='/test',
        app={'my_value': 'value1'},
        match_info={'path': '/test'},
        headers={},
        body=None
    )
    await handler(request)

    assert values == [f'{appname}: value1']

@pytest.mark.asyncio
async def test_make_handler_with_different_appnames(router):
    appname1 = "app_one"
    appname2 = "app_two"
    values1 = []
    values2 = []
    handler1 = make_handler(appname1)
    handler2 = make_handler(appname2)
    router.add_route("GET", "/test1", handler1)
    router.add_route("GET", "/test2", handler2)

    request1 = web.Request(
        method='GET',
        path='/test1',
        app={'my_value': 'value1'},
        match_info={'path': '/test1'},
        headers={},
        body=None
    )
    request2 = web.Request(
        method='GET',
        path='/test2',
        app={'my_value': 'value2'},
        match_info={'path': '/test2'},
        headers={},
        body=None
    )
    await handler1(request1)
    await handler2(request2)

    assert values1 == [f'{appname1}: value1']
    assert values2 == [f'{appname2}: value2']

@pytest.mark.asyncio
async def test_make_handler_with_missing_my_value(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = web.Request(
        method='GET',
        path='/test',
        app={},
        match_info={'path': '/test'},
        headers={},
        body=None
    )
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'  # Ensure it still returns 'Ok' even without my_value

@pytest.mark.asyncio
async def test_make_handler_duplicate_route_name(router):
    appname = "test_app"
    handler1 = make_handler(appname)
    handler2 = make_handler(appname)
    router.add_route("GET", "/duplicate", handler1, name="duplicate")

    with pytest.raises(ValueError) as ctx:
        router.add_route("GET", "/duplicate_other", handler2, name="duplicate")
    assert str(ctx.value).startswith("Duplicate 'duplicate', already handled by")