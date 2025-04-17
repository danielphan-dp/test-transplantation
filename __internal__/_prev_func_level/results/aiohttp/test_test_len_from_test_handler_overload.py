import pytest
from aiohttp import web
from aiohttp.web import Response
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await web.test_utils.make_mocked_request("GET", "/test", app=web.Application())
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_with_app_value(router):
    appname = "test_app"
    my_value = "my_value"
    app = web.Application()
    app[my_value] = "value_set"
    handler = make_handler(appname)
    app.router.add_route("GET", "/test", handler)

    request = await web.test_utils.make_mocked_request("GET", "/test", app=app)
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert f'{appname}: value_set' in request.app[my_value]

@pytest.mark.asyncio
async def test_make_handler_no_app_value(router):
    appname = "test_app"
    handler = make_handler(appname)
    app = web.Application()
    app.router.add_route("GET", "/test", handler)

    request = await web.test_utils.make_mocked_request("GET", "/test", app=app)
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert f'{appname}: None' in request.app.get('my_value', None)