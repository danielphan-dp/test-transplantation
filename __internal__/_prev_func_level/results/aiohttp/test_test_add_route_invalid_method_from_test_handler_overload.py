import pytest
from aiohttp import web
from aiohttp.web import Request
from aiohttp.test_utils import make_mocked_request

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.mark.asyncio
async def test_make_handler_valid(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler('test_app')
    request = make_mocked_request('GET', '/', app=app)
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'test_app: test_data' in values

@pytest.mark.asyncio
async def test_make_handler_no_value(app):
    my_value = 'test_value'
    handler = make_handler('test_app')
    request = make_mocked_request('GET', '/', app=app)
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'test_app: None' in values

@pytest.mark.asyncio
async def test_make_handler_invalid_appname(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler(None)
    request = make_mocked_request('GET', '/', app=app)
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert 'None: test_data' in values

@pytest.mark.asyncio
async def test_make_handler_multiple_requests(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler('test_app')
    
    for _ in range(5):
        request = make_mocked_request('GET', '/', app=app)
        response = await handler(request)
        assert response.status == 200
        assert await response.text() == 'Ok'
    
    assert len(values) == 5
    assert all('test_app: test_data' in v for v in values)