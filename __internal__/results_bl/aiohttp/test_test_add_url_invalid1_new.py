import pytest
from aiohttp import web
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.fixture
def appname():
    return "test_app"

@pytest.fixture
def my_value():
    return "my_value"

def test_make_handler_valid(router, appname, my_value):
    handler = make_handler(appname)
    router.add_route("POST", "/post/{id}", handler)
    request = web.Request(
        method='POST',
        path='/post/1',
        app=web.Application(),
        match_info={'id': '1'}
    )
    request.app[my_value] = "test_value"
    response = asyncio.run(handler(request))
    assert response.text == 'Ok'

def test_make_handler_no_value(router, appname, my_value):
    handler = make_handler(appname)
    router.add_route("POST", "/post/{id}", handler)
    request = web.Request(
        method='POST',
        path='/post/1',
        app=web.Application(),
        match_info={'id': '1'}
    )
    del request.app[my_value]
    response = asyncio.run(handler(request))
    assert response.text == 'Ok'

def test_make_handler_invalid_appname(router):
    with pytest.raises(TypeError):
        handler = make_handler(None)

def test_make_handler_invalid_request_method(router, appname):
    handler = make_handler(appname)
    router.add_route("GET", "/post/{id}", handler)
    request = web.Request(
        method='GET',
        path='/post/1',
        app=web.Application(),
        match_info={'id': '1'}
    )
    response = asyncio.run(handler(request))
    assert response.status == 405  # Method Not Allowed

def test_make_handler_multiple_requests(router, appname, my_value):
    handler = make_handler(appname)
    router.add_route("POST", "/post/{id}", handler)
    request1 = web.Request(
        method='POST',
        path='/post/1',
        app=web.Application(),
        match_info={'id': '1'}
    )
    request1.app[my_value] = "value1"
    request2 = web.Request(
        method='POST',
        path='/post/2',
        app=web.Application(),
        match_info={'id': '2'}
    )
    request2.app[my_value] = "value2"
    asyncio.run(handler(request1))
    asyncio.run(handler(request2))
    assert request1.app[my_value] == "value1"
    assert request2.app[my_value] == "value2"