import pytest
from aiohttp import web
from aiohttp.web import Request
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def app():
    return web.Application()

@pytest.mark.asyncio
async def test_make_handler_with_valid_appname(app):
    app['my_value'] = 'test_value'
    handler = make_handler('test_app')
    request = web.Request(web.View, app=app, match_info={})
    response = await handler(request)
    assert response.text == 'Ok'
    assert 'test_app: test_value' in values

@pytest.mark.asyncio
async def test_make_handler_with_empty_appname(app):
    app['my_value'] = 'test_value'
    handler = make_handler('')
    request = web.Request(web.View, app=app, match_info={})
    response = await handler(request)
    assert response.text == 'Ok'
    assert ': test_value' in values

@pytest.mark.asyncio
async def test_make_handler_with_none_appname(app):
    app['my_value'] = 'test_value'
    handler = make_handler(None)
    request = web.Request(web.View, app=app, match_info={})
    response = await handler(request)
    assert response.text == 'Ok'
    assert 'None: test_value' in values

@pytest.mark.asyncio
async def test_make_handler_with_different_app_value(app):
    app['my_value'] = 'another_value'
    handler = make_handler('test_app')
    request = web.Request(web.View, app=app, match_info={})
    response = await handler(request)
    assert response.text == 'Ok'
    assert 'test_app: another_value' in values

@pytest.mark.asyncio
async def test_make_handler_with_no_app_value(app):
    handler = make_handler('test_app')
    request = web.Request(web.View, app=app, match_info={})
    response = await handler(request)
    assert response.text == 'Ok'
    assert 'test_app: None' in values