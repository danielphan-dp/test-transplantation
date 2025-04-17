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
    assert request.app[my_value] == "test_value"

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
    assert request.app[my_value] == "test_value"

@pytest.mark.asyncio
async def test_make_handler_with_different_appname(app):
    appname = "another_app"
    my_value = "my_value"
    app[my_value] = "another_value"
    handler = make_handler(appname)
    app.router.add_get("/", handler)

    request = make_mocked_request('GET', '/')
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert request.app[my_value] == "another_value"

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
    assert my_value not in request.app  # Ensure my_value is not set in the app

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
        assert request.app[my_value] == "test_value"