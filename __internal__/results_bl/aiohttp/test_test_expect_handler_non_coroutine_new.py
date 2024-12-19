import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher
from your_module import make_handler  # Replace 'your_module' with the actual module name

@pytest.fixture
def router() -> UrlDispatcher:
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_valid_request(router: UrlDispatcher) -> None:
    my_value = 'test_value'
    appname = 'test_app'
    router.app[my_value] = 'some_value'
    handler = make_handler(appname)
    request = web.Request(method='GET', path='/', app=router.app)
    
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert f'{appname}: some_value' in values

@pytest.mark.asyncio
async def test_make_handler_missing_value(router: UrlDispatcher) -> None:
    my_value = 'test_value'
    appname = 'test_app'
    handler = make_handler(appname)
    request = web.Request(method='GET', path='/', app=router.app)
    
    with pytest.raises(KeyError):
        await handler(request)

@pytest.mark.asyncio
async def test_make_handler_empty_appname(router: UrlDispatcher) -> None:
    my_value = 'test_value'
    router.app[my_value] = 'some_value'
    appname = ''
    handler = make_handler(appname)
    request = web.Request(method='GET', path='/', app=router.app)
    
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert f'{appname}: some_value' in values

@pytest.mark.asyncio
async def test_make_handler_invalid_request_method(router: UrlDispatcher) -> None:
    my_value = 'test_value'
    appname = 'test_app'
    router.app[my_value] = 'some_value'
    handler = make_handler(appname)
    request = web.Request(method='POST', path='/', app=router.app)
    
    with pytest.raises(web.HTTPMethodNotAllowed):
        await handler(request)