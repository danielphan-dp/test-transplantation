import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher

@pytest.fixture
def router() -> UrlDispatcher:
    return web.UrlDispatcher()

def test_handler_response(router: web.UrlDispatcher) -> None:
    appname = "test_app"
    my_value = "my_key"
    router[my_value] = "test_value"
    handler = make_handler(appname)
    router.add_route("GET", "/get1", handler, name="name1")
    
    request = web.Request(method='GET', path='/get1', app=router)
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert "test_app: test_value" in values

def test_handler_with_different_appname(router: web.UrlDispatcher) -> None:
    appname = "another_app"
    my_value = "my_key"
    router[my_value] = "another_value"
    handler = make_handler(appname)
    router.add_route("GET", "/get2", handler, name="name2")
    
    request = web.Request(method='GET', path='/get2', app=router)
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert "another_app: another_value" in values

def test_handler_no_value(router: web.UrlDispatcher) -> None:
    appname = "no_value_app"
    my_value = "my_key"
    router[my_value] = None
    handler = make_handler(appname)
    router.add_route("GET", "/get3", handler, name="name3")
    
    request = web.Request(method='GET', path='/get3', app=router)
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert "no_value_app: None" in values

def test_handler_invalid_route(router: web.UrlDispatcher) -> None:
    appname = "invalid_route_app"
    handler = make_handler(appname)
    
    request = web.Request(method='GET', path='/invalid', app=router)
    response = await handler(request)
    
    assert response.status == 404