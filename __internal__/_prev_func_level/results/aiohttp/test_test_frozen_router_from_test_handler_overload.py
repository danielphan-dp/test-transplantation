import pytest
from aiohttp import web
from aiohttp.test_utils import AiohttpClient

@pytest.fixture
def app():
    app = web.Application()
    app['my_value'] = 'test_value'
    return app

async def test_make_handler(aiohttp_client, app):
    handler = make_handler("test_app")
    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert 'test_app: test_value' in values

async def test_make_handler_no_value(aiohttp_client, app):
    app['my_value'] = None
    handler = make_handler("test_app")
    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert 'test_app: None' in values

async def test_make_handler_empty_appname(aiohttp_client, app):
    handler = make_handler("")
    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert ': test_value' in values

async def test_make_handler_frozen_router(aiohttp_client, app):
    app.router.freeze()
    handler = make_handler("test_app")
    with pytest.raises(RuntimeError):
        app.router.add_get("/", handler)