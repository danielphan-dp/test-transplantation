import pytest
from aiohttp import web
from aiohttp.test_utils import AiohttpClient

@pytest.fixture
async def app():
    app = web.Application()
    app['my_value'] = 'test_value'
    return app

async def test_make_handler_get(app: web.Application, aiohttp_client: AiohttpClient) -> None:
    handler = make_handler('test_app')
    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert 'test_app: test_value' in values

async def test_make_handler_post(app: web.Application, aiohttp_client: AiohttpClient) -> None:
    handler = make_handler('test_app')
    app.router.add_post("/", handler)
    client = await aiohttp_client(app)

    resp = await client.post("/")
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert 'test_app: test_value' in values

async def test_make_handler_no_app_value(app: web.Application, aiohttp_client: AiohttpClient) -> None:
    app['my_value'] = None
    handler = make_handler('test_app')
    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == 'Ok'
    assert 'test_app: None' in values

async def test_make_handler_invalid_method(app: web.Application, aiohttp_client: AiohttpClient) -> None:
    handler = make_handler('test_app')
    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    resp = await client.post("/")
    assert resp.status == 405  # Method Not Allowed

async def test_make_handler_multiple_requests(app: web.Application, aiohttp_client: AiohttpClient) -> None:
    handler = make_handler('test_app')
    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    for _ in range(5):
        resp = await client.get("/")
        assert resp.status == 200
        assert await resp.text() == 'Ok'
    
    assert len(values) == 5
    assert all('test_app: test_value' in v for v in values)