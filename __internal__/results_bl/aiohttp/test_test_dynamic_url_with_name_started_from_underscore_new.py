import pytest
from aiohttp import web
from aiohttp.web import Response
from aiohttp.test_utils import make_mocked_request
from yarl import URL

values = []

def make_handler(appname: str) -> web.Handler:
    async def handler(request: web.Request) -> web.Response:
        values.append(f'{appname}: {request.app["my_value"]}')
        return web.Response(text='Ok')
    return handler

@pytest.fixture
def router():
    return web.UrlDispatcher()

def test_dynamic_url_with_name_started_from_underscore(router):
    route = router.add_route("GET", "/get/{_name}", make_handler("test_app"))
    assert URL("/get/John") == route.url_for(_name="John")

def test_dynamic_url_with_empty_name(router):
    route = router.add_route("GET", "/get/{_name}", make_handler("test_app"))
    assert URL("/get/") == route.url_for(_name="")

def test_dynamic_url_with_special_characters(router):
    route = router.add_route("GET", "/get/{_name}", make_handler("test_app"))
    assert URL("/get/%20") == route.url_for(_name=" ")

def test_dynamic_url_with_numeric_name(router):
    route = router.add_route("GET", "/get/{_name}", make_handler("test_app"))
    assert URL("/get/123") == route.url_for(_name="123")

def test_dynamic_url_with_long_name(router):
    long_name = "a" * 100
    route = router.add_route("GET", "/get/{_name}", make_handler("test_app"))
    assert URL(f"/get/{long_name}") == route.url_for(_name=long_name)

def test_handler_response(router):
    app = web.Application()
    app["my_value"] = "value"
    handler = make_handler("test_app")
    app.router.add_route("GET", "/get/{_name}", handler)
    request = make_mocked_request("GET", "/get/John", app=app)
    response = await handler(request)
    assert response.text == 'Ok'
    assert values == ['test_app: value']