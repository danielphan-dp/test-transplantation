import pytest
from aiohttp import web
from aiohttp.web import Request
from aiohttp.test_utils import make_mocked_request
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.mark.asyncio
async def test_make_handler_valid_request():
    appname = "test_app"
    handler = make_handler(appname)
    request = make_mocked_request('GET', '/', app={'my_value': 'test_value'})
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert f'{appname}: test_value' in request.app['my_value']

@pytest.mark.asyncio
async def test_make_handler_no_my_value():
    appname = "test_app"
    handler = make_handler(appname)
    request = make_mocked_request('GET', '/', app={})
    
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert f'{appname}: None' in request.app.get('my_value', 'None')

@pytest.mark.asyncio
async def test_make_handler_invalid_method():
    appname = "test_app"
    handler = make_handler(appname)
    request = make_mocked_request('POST', '/', app={'my_value': 'test_value'})
    
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert f'{appname}: test_value' in request.app['my_value']

@pytest.mark.asyncio
async def test_make_handler_empty_appname():
    appname = ""
    handler = make_handler(appname)
    request = make_mocked_request('GET', '/', app={'my_value': 'test_value'})
    
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert f'{appname}: test_value' in request.app['my_value']