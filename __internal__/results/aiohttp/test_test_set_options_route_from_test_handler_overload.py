import pytest
from aiohttp import web
from aiohttp.web import Request
from aiohttp.test_utils import make_mocked_request

@pytest.fixture
def app():
    app = web.Application()
    app['my_value'] = 'test_value'
    return app

@pytest.fixture
def client(aiohttp_client, app):
    return aiohttp_client(app)

async def test_make_handler(client):
    handler = make_handler("test_app")
    app = client.app
    app.router.add_get('/test', handler)

    request = make_mocked_request('GET', '/test', app=app)
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'test_app: test_value' in app['my_value']

async def test_make_handler_no_value(client):
    handler = make_handler("test_app")
    app = client.app
    app['my_value'] = None
    app.router.add_get('/test', handler)

    request = make_mocked_request('GET', '/test', app=app)
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'test_app: None' in app['my_value']

async def test_make_handler_invalid_request(client):
    handler = make_handler("test_app")
    app = client.app
    app.router.add_post('/test', handler)

    request = make_mocked_request('POST', '/test', app=app)
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'test_app: test_value' in app['my_value']