import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher
from your_module import make_handler  # Replace 'your_module' with the actual module name

@pytest.fixture
def app():
    app = web.Application()
    app['my_value'] = 'test_value'
    return app

@pytest.mark.asyncio
async def test_make_handler(app):
    handler = make_handler("test_app")
    request = web.Request(method='GET', path='/', app=app)
    response = await handler(request)
    
    assert response.status == 200
    assert response.text == 'Ok'
    assert 'test_app: test_value' in app['my_value']

@pytest.mark.asyncio
async def test_make_handler_no_app_value():
    handler = make_handler("test_app")
    app = web.Application()
    request = web.Request(method='GET', path='/', app=app)
    
    with pytest.raises(KeyError):
        await handler(request)

@pytest.mark.asyncio
async def test_make_handler_empty_appname(app):
    handler = make_handler("")
    request = web.Request(method='GET', path='/', app=app)
    response = await handler(request)
    
    assert response.status == 200
    assert response.text == 'Ok'
    assert '' in app['my_value']