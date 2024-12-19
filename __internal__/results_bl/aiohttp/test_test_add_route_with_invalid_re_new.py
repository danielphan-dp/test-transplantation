import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import PATH_SEP
from your_module import make_handler  # Replace 'your_module' with the actual module name

@pytest.fixture
def router():
    return web.UrlDispatcher()

def test_make_handler_valid_request(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/handler", handler)
    request = web.Request(method="GET", path="/handler", app={"my_value": "test_value"})
    response = asyncio.run(handler(request))
    assert response.text == 'Ok'

def test_make_handler_invalid_appname(router):
    appname = ""
    handler = make_handler(appname)
    router.add_route("GET", "/handler", handler)
    request = web.Request(method="GET", path="/handler", app={"my_value": "test_value"})
    response = asyncio.run(handler(request))
    assert response.text == 'Ok'

def test_make_handler_no_my_value(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/handler", handler)
    request = web.Request(method="GET", path="/handler", app={})
    response = asyncio.run(handler(request))
    assert response.text == 'Ok'

def test_make_handler_with_special_characters(router):
    appname = "test_app!@#"
    handler = make_handler(appname)
    router.add_route("GET", "/handler", handler)
    request = web.Request(method="GET", path="/handler", app={"my_value": "special_value"})
    response = asyncio.run(handler(request))
    assert response.text == 'Ok'