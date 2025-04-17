import pytest
from aiohttp import web
from aiohttp.web import Response
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.mark.asyncio
async def test_make_handler_with_valid_appname(app):
    appname = "test_app"
    handler = make_handler(appname)
    app.router.add_get("/test", handler)

    client = await aiohttp_client(app)
    resp = await client.get("/test")
    assert resp.status == 200
    text = await resp.text()
    assert text == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_with_different_appname(app):
    appname = "another_app"
    handler = make_handler(appname)
    app.router.add_get("/test2", handler)

    client = await aiohttp_client(app)
    resp = await client.get("/test2")
    assert resp.status == 200
    text = await resp.text()
    assert text == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_with_no_appname(app):
    appname = ""
    handler = make_handler(appname)
    app.router.add_get("/test3", handler)

    client = await aiohttp_client(app)
    resp = await client.get("/test3")
    assert resp.status == 200
    text = await resp.text()
    assert text == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_with_invalid_request(app):
    appname = "test_app"
    handler = make_handler(appname)
    app.router.add_get("/test_invalid", handler)

    client = await aiohttp_client(app)
    resp = await client.get("/test_invalid", params={"invalid_param": "value"})
    assert resp.status == 200
    text = await resp.text()
    assert text == 'Ok'