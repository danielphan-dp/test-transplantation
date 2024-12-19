import pytest
from aiohttp import web
from your_module import make_handler  # Replace 'your_module' with the actual module name

@pytest.fixture
def app():
    return web.Application()

@pytest.fixture
def handler(app):
    appname = "test_app"
    return make_handler(appname)

def test_handler_returns_ok(handler):
    request = web.Request(web.HTTPrequest(), 'GET', '/test', app=web.Application())
    response = await handler(request)
    assert response.status == 200
    assert response.text == 'Ok'

def test_handler_includes_appname(handler):
    request = web.Request(web.HTTPrequest(), 'GET', '/test', app=web.Application())
    values = []
    request.app['my_value'] = 'test_value'
    response = await handler(request)
    assert 'test_app: test_value' in values

def test_handler_with_missing_my_value(handler):
    request = web.Request(web.HTTPrequest(), 'GET', '/test', app=web.Application())
    request.app.pop('my_value', None)
    with pytest.raises(KeyError):
        await handler(request)

def test_handler_with_invalid_appname():
    with pytest.raises(TypeError):
        make_handler(None)

def test_handler_with_empty_appname():
    handler = make_handler("")
    request = web.Request(web.HTTPrequest(), 'GET', '/test', app=web.Application())
    response = await handler(request)
    assert response.status == 200
    assert response.text == 'Ok'