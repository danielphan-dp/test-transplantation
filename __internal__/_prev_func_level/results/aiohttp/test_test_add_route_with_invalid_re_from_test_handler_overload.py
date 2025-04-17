import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import PATH_SEP
from your_module import make_handler  # Replace with the actual module name

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
        method='GET',
        path='/',
        app=app,
        match_info=web.MatchInfo({'param': 'value'}),
        headers={},
    )
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'my_app: test_data' in values

@pytest.mark.asyncio
async def test_make_handler_no_app_value(app):
    my_value = 'test_value'
    handler = make_handler('my_app')

    request = web.Request(
        method='GET',
        path='/',
        app=app,
        match_info=web.MatchInfo({'param': 'value'}),
        headers={},
    )
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'my_app: None' in values

@pytest.mark.asyncio
async def test_make_handler_invalid_appname(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler('')

    request = web.Request(
        method='GET',
        path='/',
        app=app,
        match_info=web.MatchInfo({'param': 'value'}),
        headers={},
    )
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert ': test_data' in values

@pytest.mark.asyncio
async def test_make_handler_with_special_characters(app):
    my_value = 'test_value'
    app[my_value] = 'special_data'
    handler = make_handler('my_app!@#')

    request = web.Request(
        method='GET',
        path='/',
        app=app,
        match_info=web.MatchInfo({'param': 'value'}),
        headers={},
    )
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'my_app!@#: special_data' in values

@pytest.mark.asyncio
async def test_make_handler_multiple_requests(app):
    my_value = 'test_value'
    app[my_value] = 'data1'
    handler = make_handler('app1')

    request1 = web.Request(
        method='GET',
        path='/',
        app=app,
        match_info=web.MatchInfo({'param': 'value'}),
        headers={},
    )
    await handler(request1)

    app[my_value] = 'data2'
    handler = make_handler('app2')
    request2 = web.Request(
        method='GET',
        path='/',
        app=app,
        match_info=web.MatchInfo({'param': 'value'}),
        headers={},
    )
    response = await handler(request2)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'app2: data2' in values