import pytest
from aiohttp import web
from aiohttp.web import Request
from your_module import make_handler  # Replace with the actual module name

@pytest.fixture
def app():
    app = web.Application()
    app['my_value'] = 'test_value'
    return app

@pytest.mark.asyncio
async def test_make_handler(app):
    handler = make_handler("test_app")
    app.router.add_get('/test', handler)

    request = Request(method='GET', path='/test', app=app)
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'test_app: test_value' in app['my_value']

@pytest.mark.asyncio
async def test_make_handler_with_different_appname(app):
    handler = make_handler("another_app")
    app.router.add_get('/another', handler)

    request = Request(method='GET', path='/another', app=app)
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'another_app: test_value' in app['my_value']

@pytest.mark.asyncio
async def test_make_handler_with_no_appname(app):
    handler = make_handler("")
    app.router.add_get('/empty', handler)

    request = Request(method='GET', path='/empty', app=app)
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert ': test_value' in app['my_value']