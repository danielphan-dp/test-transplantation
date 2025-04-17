import pytest
from aiohttp import web
from aiohttp.web import Response
from aiohttp.test_utils import make_mocked_request

@pytest.fixture
def app():
    app = web.Application()
    return app

def make_handler(appname: str):
    async def handler(request: web.Request) -> web.Response:
        return Response(text=f'{appname}: {request.app["my_value"]}')
    return handler

async def test_handler_with_valid_appname(app):
    app["my_value"] = "test_value"
    app.router.add_get("/test/{name}", make_handler("TestApp"))
    request = make_mocked_request("GET", "/test/John", app=app)
    response = await app.router[0].handler(request)
    assert response.status == 200
    assert await response.text() == "TestApp: test_value"

async def test_handler_with_missing_my_value(app):
    app.router.add_get("/test/{name}", make_handler("TestApp"))
    request = make_mocked_request("GET", "/test/John", app=app)
    response = await app.router[0].handler(request)
    assert response.status == 200
    assert await response.text() == "TestApp: None"

async def test_handler_with_different_appname(app):
    app["my_value"] = "another_value"
    app.router.add_get("/test/{name}", make_handler("AnotherApp"))
    request = make_mocked_request("GET", "/test/John", app=app)
    response = await app.router[0].handler(request)
    assert response.status == 200
    assert await response.text() == "AnotherApp: another_value"

async def test_handler_with_empty_appname(app):
    app["my_value"] = "empty_value"
    app.router.add_get("/test/{name}", make_handler(""))
    request = make_mocked_request("GET", "/test/John", app=app)
    response = await app.router[0].handler(request)
    assert response.status == 200
    assert await response.text() == ": empty_value"