import pytest
from aiohttp import web
from your_module import make_handler  # Replace 'your_module' with the actual module name

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_valid(router):
    appname = "test_app"
    my_value = "test_value"
    router[my_value] = "value_set"
    handler = make_handler(appname)
    request = web.Request(method='GET', path='/', app=router)
    response = await handler(request)
    assert response.text == 'Ok'
    assert f'{appname}: value_set' in values

@pytest.mark.asyncio
async def test_make_handler_no_app_value(router):
    appname = "test_app"
    my_value = "test_value"
    handler = make_handler(appname)
    request = web.Request(method='GET', path='/', app=router)
    response = await handler(request)
    assert response.text == 'Ok'
    assert f'{appname}: None' in values

@pytest.mark.asyncio
async def test_make_handler_invalid_appname(router):
    appname = None
    my_value = "test_value"
    router[my_value] = "value_set"
    handler = make_handler(appname)
    request = web.Request(method='GET', path='/', app=router)
    response = await handler(request)
    assert response.text == 'Ok'
    assert f'None: value_set' in values

@pytest.mark.asyncio
async def test_make_handler_empty_appname(router):
    appname = ""
    my_value = "test_value"
    router[my_value] = "value_set"
    handler = make_handler(appname)
    request = web.Request(method='GET', path='/', app=router)
    response = await handler(request)
    assert response.text == 'Ok'
    assert f' : value_set' in values

@pytest.mark.asyncio
async def test_make_handler_invalid_route(router):
    appname = "test_app"
    handler = make_handler(appname)
    with pytest.raises(ValueError):
        router.add_route("post", "/post/{id{}}", handler)