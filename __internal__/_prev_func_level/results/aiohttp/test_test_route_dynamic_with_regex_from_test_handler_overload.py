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
    app['my_value'] = 'test_value'
    handler = make_handler('test_app')
    app.router.add_get('/test', handler)

    request = await app.test_client.get('/test')
    assert request.status == 200
    assert await request.text() == 'Ok'
    assert 'test_app: test_value' in values

@pytest.mark.asyncio
async def test_make_handler_with_empty_appname(app):
    app['my_value'] = 'test_value'
    handler = make_handler('')
    app.router.add_get('/test', handler)

    request = await app.test_client.get('/test')
    assert request.status == 200
    assert await request.text() == 'Ok'
    assert ': test_value' in values

@pytest.mark.asyncio
async def test_make_handler_with_nonexistent_key(app):
    handler = make_handler('test_app')
    app.router.add_get('/test', handler)

    request = await app.test_client.get('/test')
    assert request.status == 200
    assert await request.text() == 'Ok'
    assert 'test_app: ' in values

@pytest.mark.asyncio
async def test_make_handler_with_special_characters(app):
    app['my_value'] = 'value_with_special_chars!@#'
    handler = make_handler('test_app')
    app.router.add_get('/test', handler)

    request = await app.test_client.get('/test')
    assert request.status == 200
    assert await request.text() == 'Ok'
    assert 'test_app: value_with_special_chars!@#' in values

@pytest.mark.asyncio
async def test_make_handler_multiple_requests(app):
    app['my_value'] = 'test_value'
    handler = make_handler('test_app')
    app.router.add_get('/test', handler)

    for _ in range(5):
        request = await app.test_client.get('/test')
        assert request.status == 200
        assert await request.text() == 'Ok'
    
    assert values == ['test_app: test_value'] * 5