import pytest
from aiohttp import web
from aiohttp.web import Request

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.mark.asyncio
async def test_make_handler_valid(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler('my_app')
    
    request = web.Request(
        app=app,
        match_info={},
        method='GET',
        path='/',
        headers={},
        query_string='',
        body=b''
    )
    
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_invalid_appname(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler('')
    
    request = web.Request(
        app=app,
        match_info={},
        method='GET',
        path='/',
        headers={},
        query_string='',
        body=b''
    )
    
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_no_app_value(app):
    my_value = 'test_value'
    handler = make_handler('my_app')
    
    request = web.Request(
        app=app,
        match_info={},
        method='GET',
        path='/',
        headers={},
        query_string='',
        body=b''
    )
    
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_multiple_requests(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler('my_app')
    
    request1 = web.Request(
        app=app,
        match_info={},
        method='GET',
        path='/',
        headers={},
        query_string='',
        body=b''
    )
    
    request2 = web.Request(
        app=app,
        match_info={},
        method='GET',
        path='/',
        headers={},
        query_string='',
        body=b''
    )
    
    response1 = await handler(request1)
    response2 = await handler(request2)
    
    assert response1.status == 200
    assert await response1.text() == 'Ok'
    assert response2.status == 200
    assert await response2.text() == 'Ok'