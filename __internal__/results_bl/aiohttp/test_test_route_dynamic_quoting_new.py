import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router():
    return UrlDispatcher()

@pytest.mark.asyncio
async def test_handler_with_valid_appname(router):
    values = []
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test/{arg}", handler)

    request = await router["/test/1"].get()
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert values == [f'{appname}: {request.app["my_value"]}']

@pytest.mark.asyncio
async def test_handler_with_empty_appname(router):
    values = []
    appname = ""
    handler = make_handler(appname)
    router.add_route("GET", "/test/{arg}", handler)

    request = await router["/test/1"].get()
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert values == [f'{appname}: {request.app["my_value"]}']

@pytest.mark.asyncio
async def test_handler_with_special_characters(router):
    values = []
    appname = "test@#app"
    handler = make_handler(appname)
    router.add_route("GET", "/test/{arg}", handler)

    request = await router["/test/1"].get()
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert values == [f'{appname}: {request.app["my_value"]}']

@pytest.mark.asyncio
async def test_handler_with_nonexistent_appname(router):
    values = []
    appname = "nonexistent_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test/{arg}", handler)

    request = await router["/test/1"].get()
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert values == [f'{appname}: {request.app.get("my_value", "default_value")}']