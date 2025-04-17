import pytest
from aiohttp import web
from aiohttp.web import Response
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.fixture
def client(aiohttp_client, app):
    return aiohttp_client(app)

async def test_make_handler(client):
    appname = "test_app"
    handler = make_handler(appname)
    client.app.router.add_get("/test", handler)

    request = await client.get("/test")
    assert request.status == 200
    assert await request.text() == 'Ok'

async def test_make_handler_with_app_value(client):
    appname = "test_app"
    my_value = "my_value"
    client.app[my_value] = "value_set"
    handler = make_handler(appname)
    client.app.router.add_get("/test", handler)

    request = await client.get("/test")
    assert request.status == 200
    assert await request.text() == 'Ok'
    assert f'{appname}: value_set' in client.app['values']

async def test_make_handler_no_app_value(client):
    appname = "test_app"
    handler = make_handler(appname)
    client.app.router.add_get("/test", handler)

    request = await client.get("/test")
    assert request.status == 200
    assert await request.text() == 'Ok'
    assert f'{appname}: None' in client.app['values']

async def test_make_handler_multiple_requests(client):
    appname = "test_app"
    handler = make_handler(appname)
    client.app.router.add_get("/test", handler)

    for _ in range(5):
        request = await client.get("/test")
        assert request.status == 200
        assert await request.text() == 'Ok'

    assert len(client.app['values']) == 5
    assert all(f'{appname}: None' in value for value in client.app['values'])