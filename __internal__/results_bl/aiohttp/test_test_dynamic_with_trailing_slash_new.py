import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import Resource
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router():
    return web.UrlDispatcher()

def test_handler_response(router):
    appname = "TestApp"
    handler = make_handler(appname)
    router.add_route("GET", "/get/{name}/", handler, name="name")
    request = web.Request(web.HTTPrequest, "GET", "/get/John/")
    response = await handler(request)
    assert response.text == 'Ok'

def test_handler_with_different_name(router):
    appname = "AnotherApp"
    handler = make_handler(appname)
    router.add_route("GET", "/get/{name}/", handler, name="name")
    request = web.Request(web.HTTPrequest, "GET", "/get/Jane/")
    response = await handler(request)
    assert response.text == 'Ok'

def test_handler_with_empty_name(router):
    appname = "EmptyNameApp"
    handler = make_handler(appname)
    router.add_route("GET", "/get/{name}/", handler, name="name")
    request = web.Request(web.HTTPrequest, "GET", "/get//")
    response = await handler(request)
    assert response.text == 'Ok'

def test_handler_with_special_characters(router):
    appname = "SpecialCharApp"
    handler = make_handler(appname)
    router.add_route("GET", "/get/{name}/", handler, name="name")
    request = web.Request(web.HTTPrequest, "GET", "/get/John%20Doe/")
    response = await handler(request)
    assert response.text == 'Ok'

def test_handler_invalid_method(router):
    appname = "InvalidMethodApp"
    handler = make_handler(appname)
    router.add_route("POST", "/get/{name}/", handler, name="name")
    request = web.Request(web.HTTPrequest, "POST", "/get/John/")
    response = await handler(request)
    assert response.status == 405  # Method Not Allowed

def test_handler_no_name_parameter(router):
    appname = "NoNameParamApp"
    handler = make_handler(appname)
    router.add_route("GET", "/get/", handler, name="name")
    request = web.Request(web.HTTPrequest, "GET", "/get/")
    response = await handler(request)
    assert response.status == 404  # Not Found