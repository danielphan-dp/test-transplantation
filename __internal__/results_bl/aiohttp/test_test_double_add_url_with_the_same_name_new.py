import pytest
from aiohttp import web
from your_module import make_handler  # Replace 'your_module' with the actual module name

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_handler_returns_ok(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await web.test_utils.make_mocked_request("GET", "/test", app=web.Application())
    response = await handler(request)

    assert response.status == 200
    assert response.text == 'Ok'

@pytest.mark.asyncio
async def test_handler_appname_includes_value(router):
    appname = "test_app"
    my_value = "my_key"
    values = []
    app = web.Application()
    app[my_value] = "test_value"
    handler = make_handler(appname)

    router.add_route("GET", "/test", handler)

    request = await web.test_utils.make_mocked_request("GET", "/test", app=app)
    await handler(request)

    assert values[0] == 'test_app: test_value'

@pytest.mark.asyncio
async def test_handler_with_different_appnames(router):
    handler1 = make_handler("app_one")
    handler2 = make_handler("app_two")
    router.add_route("GET", "/app_one", handler1)
    router.add_route("GET", "/app_two", handler2)

    request1 = await web.test_utils.make_mocked_request("GET", "/app_one", app=web.Application())
    request2 = await web.test_utils.make_mocked_request("GET", "/app_two", app=web.Application())

    response1 = await handler1(request1)
    response2 = await handler2(request2)

    assert response1.status == 200
    assert response2.status == 200

@pytest.mark.asyncio
async def test_handler_duplicate_route_name(router):
    handler1 = make_handler("app_one")
    handler2 = make_handler("app_two")
    router.add_route("GET", "/duplicate", handler1, name="duplicate")

    with pytest.raises(ValueError) as ctx:
        router.add_route("GET", "/duplicate_other", handler2, name="duplicate")
    assert str(ctx.value).startswith("Duplicate 'duplicate', already handled by")