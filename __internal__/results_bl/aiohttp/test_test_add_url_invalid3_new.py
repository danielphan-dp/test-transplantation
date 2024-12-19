import pytest
from aiohttp import web
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router():
    return web.UrlDispatcher()

def test_make_handler_valid(router):
    appname = "test_app"
    my_value = "key"
    router[my_value] = "value"
    handler = make_handler(appname)
    request = web.Request(method='GET', path='/', app=router)
    response = asyncio.run(handler(request))
    assert response.text == 'Ok'
    assert f'{appname}: value' in values

def test_make_handler_no_app_value(router):
    appname = "test_app"
    my_value = "key"
    handler = make_handler(appname)
    request = web.Request(method='GET', path='/', app=router)
    response = asyncio.run(handler(request))
    assert response.text == 'Ok'
    assert f'{appname}: None' in values

def test_make_handler_empty_appname(router):
    appname = ""
    my_value = "key"
    router[my_value] = "value"
    handler = make_handler(appname)
    request = web.Request(method='GET', path='/', app=router)
    response = asyncio.run(handler(request))
    assert response.text == 'Ok'
    assert f'{appname}: value' in values

def test_make_handler_invalid_request_method(router):
    appname = "test_app"
    my_value = "key"
    router[my_value] = "value"
    handler = make_handler(appname)
    request = web.Request(method='PUT', path='/', app=router)
    response = asyncio.run(handler(request))
    assert response.text == 'Ok'
    assert f'{appname}: value' in values

def test_make_handler_multiple_requests(router):
    appname = "test_app"
    my_value = "key"
    router[my_value] = "value"
    handler = make_handler(appname)
    
    for _ in range(5):
        request = web.Request(method='GET', path='/', app=router)
        response = asyncio.run(handler(request))
        assert response.text == 'Ok'
    
    assert values.count(f'{appname}: value') == 5