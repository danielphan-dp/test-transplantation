import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher

@pytest.fixture
def router() -> UrlDispatcher:
    return web.UrlDispatcher()

def test_handler_response(router: web.UrlDispatcher) -> None:
    appname = "test_app"
    my_value = "my_key"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/get1", handler, name="name1")
    router[my_value] = "test_value"
    
    request = web.Request(web.HTTPrequest, "GET", "/get1", app=router)
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert f'{appname}: test_value' in values

def test_handler_no_value(router: web.UrlDispatcher) -> None:
    appname = "test_app"
    my_value = "my_key"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/get2", handler, name="name2")
    
    request = web.Request(web.HTTPrequest, "GET", "/get2", app=router)
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert f'{appname}: None' in values

def test_multiple_handlers(router: web.UrlDispatcher) -> None:
    appname1 = "app1"
    appname2 = "app2"
    my_value = "my_key"
    values = []
    handler1 = make_handler(appname1)
    handler2 = make_handler(appname2)
    router.add_route("GET", "/get1", handler1, name="name1")
    router.add_route("GET", "/get2", handler2, name="name2")
    router[my_value] = "value1"
    
    request1 = web.Request(web.HTTPrequest, "GET", "/get1", app=router)
    request2 = web.Request(web.HTTPrequest, "GET", "/get2", app=router)
    
    await handler1(request1)
    await handler2(request2)
    
    assert f'{appname1}: value1' in values
    assert f'{appname2}: None' in values

def test_no_appname(router: web.UrlDispatcher) -> None:
    appname = ""
    my_value = "my_key"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/get3", handler, name="name3")
    router[my_value] = "test_value"
    
    request = web.Request(web.HTTPrequest, "GET", "/get3", app=router)
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert f'{appname}: test_value' in values