import pytest
from aiohttp import web
from aiohttp.web import Request
from aiohttp.test_utils import make_mocked_request
from your_module import make_handler  # Replace with the actual module name

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.fixture
def router(app):
    return app.router

async def test_make_handler_returns_ok(router):
    my_value = 'test_value'
    appname = 'test_app'
    handler = make_handler(appname)
    router.add_route("GET", "/", handler)

    request = make_mocked_request('GET', '/', app=app)
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'

async def test_make_handler_inserts_value(router):
    my_value = 'test_value'
    appname = 'test_app'
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/", handler)

    request = make_mocked_request('GET', '/', app=app)
    request.app[my_value] = 'some_value'
    await handler(request)

    assert values == [f'{appname}: some_value']

async def test_make_handler_with_different_appname(router):
    my_value = 'test_value'
    appname = 'another_app'
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/", handler)

    request = make_mocked_request('GET', '/', app=app)
    request.app[my_value] = 'different_value'
    await handler(request)

    assert values == [f'{appname}: different_value']

async def test_make_handler_with_no_value(router):
    my_value = 'test_value'
    appname = 'test_app'
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/", handler)

    request = make_mocked_request('GET', '/', app=app)
    request.app[my_value] = None
    await handler(request)

    assert values == [f'{appname}: None']