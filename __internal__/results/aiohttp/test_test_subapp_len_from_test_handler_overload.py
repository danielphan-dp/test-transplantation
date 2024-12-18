import pytest
from aiohttp import web
from aiohttp.web import Response
from aiohttp.test_utils import make_mocked_request
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def app():
    return web.Application()

@pytest.mark.asyncio
async def test_make_handler_get(app):
    appname = "test_app"
    my_value = "my_value"
    app[my_value] = "test_value"
    handler = make_handler(appname)
    app.router.add_get("/", handler)

    request = make_mocked_request('GET', '/')
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert f'{appname}: test_value' in request.app[my_value]

@pytest.mark.asyncio
async def test_make_handler_post(app):
    appname = "test_app"
    my_value = "my_value"
    app[my_value] = "test_value"
    handler = make_handler(appname)
    app.router.add_post("/", handler)

    request = make_mocked_request('POST', '/')
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert f'{appname}: test_value' in request.app[my_value]

@pytest.mark.asyncio
async def test_make_handler_no_value(app):
    appname = "test_app"
    my_value = "my_value"
    handler = make_handler(appname)
    app.router.add_get("/", handler)

    request = make_mocked_request('GET', '/')
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert f'{appname}: None' in request.app.get(my_value, None)

@pytest.mark.asyncio
async def test_make_handler_invalid_method(app):
    appname = "test_app"
    handler = make_handler(appname)
    app.router.add_get("/", handler)

    request = make_mocked_request('PUT', '/')
    response = await handler(request)

    assert response.status == 405  # Method Not Allowed

@pytest.mark.asyncio
async def test_make_handler_multiple_requests(app):
    appname = "test_app"
    my_value = "my_value"
    app[my_value] = "test_value"
    handler = make_handler(appname)
    app.router.add_get("/", handler)

    for _ in range(5):
        request = make_mocked_request('GET', '/')
        response = await handler(request)
        assert response.status == 200
        assert await response.text() == 'Ok'
        assert f'{appname}: test_value' in request.app[my_value]