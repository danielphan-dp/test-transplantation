import pytest
from aiohttp import web
from aiohttp.web import Response
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def app():
    app = web.Application()
    app[my_value] = "test_value"
    return app

@pytest.mark.asyncio
async def test_make_handler(app):
    handler = make_handler("test_app")
    app.router.add_get("/test", handler)

    request = await app.test_client.get("/test")
    assert request.status == 200
    assert await request.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_with_different_appname(app):
    handler = make_handler("another_app")
    app.router.add_get("/test2", handler)

    request = await app.test_client.get("/test2")
    assert request.status == 200
    assert await request.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_appname_in_values(app):
    values = []
    handler = make_handler("test_app")
    app.router.add_get("/test3", handler)

    request = await app.test_client.get("/test3")
    assert request.status == 200
    assert await request.text() == 'Ok'
    assert f'test_app: test_value' in values

@pytest.mark.asyncio
async def test_make_handler_no_appname(app):
    handler = make_handler("")
    app.router.add_get("/test4", handler)

    request = await app.test_client.get("/test4")
    assert request.status == 200
    assert await request.text() == 'Ok'