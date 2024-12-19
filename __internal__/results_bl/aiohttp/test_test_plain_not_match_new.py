import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import make_handler

@pytest.fixture
def router():
    return web.UrlDispatcher()

def test_handler_response(router):
    appname = "test_app"
    my_value = "my_key"
    router[my_value] = "test_value"
    handler = make_handler(appname)
    router.add_route("GET", "/get/path", handler, name="name")
    
    request = web.Request(
        method='GET',
        path='/get/path',
        app=router
    )
    response = await handler(request)
    assert response.text == 'Ok'

def test_handler_value_storage(router):
    appname = "test_app"
    my_value = "my_key"
    values = []
    router[my_value] = "test_value"
    handler = make_handler(appname)
    router.add_route("GET", "/get/path", handler, name="name")
    
    request = web.Request(
        method='GET',
        path='/get/path',
        app=router
    )
    await handler(request)
    assert values == [f'{appname}: test_value']

def test_handler_invalid_route(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/get/path", handler, name="name")
    
    request = web.Request(
        method='GET',
        path='/invalid/path',
        app=router
    )
    response = await handler(request)
    assert response.status == 404

def test_handler_no_app_value(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/get/path", handler, name="name")
    
    request = web.Request(
        method='GET',
        path='/get/path',
        app=router
    )
    response = await handler(request)
    assert response.text == 'Ok'  # Ensure it still responds correctly even without the app value.