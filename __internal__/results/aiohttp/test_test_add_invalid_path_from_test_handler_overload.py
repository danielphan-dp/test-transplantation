import pytest
from aiohttp import web
from aiohttp.web import Request
from your_module import make_handler  # Replace with the actual module name

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.mark.asyncio
async def test_make_handler_valid_request(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler('test_app')
    app.router.add_get('/', handler)
    
    client = await web.test_client(app)
    resp = await client.get('/')
    
    assert resp.status == 200
    assert await resp.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_invalid_request(app):
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler('test_app')
    app.router.add_get('/invalid', handler)
    
    client = await web.test_client(app)
    resp = await client.get('/nonexistent')
    
    assert resp.status == 404

@pytest.mark.asyncio
async def test_make_handler_with_different_appname(app):
    my_value = 'test_value'
    app[my_value] = 'another_test_data'
    handler = make_handler('another_app')
    app.router.add_get('/', handler)
    
    client = await web.test_client(app)
    resp = await client.get('/')
    
    assert resp.status == 200
    assert await resp.text() == 'Ok'  # Ensure response is still 'Ok'

@pytest.mark.asyncio
async def test_make_handler_appname_in_values(app):
    values = []
    my_value = 'test_value'
    app[my_value] = 'test_data'
    handler = make_handler('test_app')
    app.router.add_get('/', handler)
    
    client = await web.test_client(app)
    await client.get('/')
    
    assert 'test_app: test_data' in values  # Check if values were appended correctly

@pytest.mark.asyncio
async def test_make_handler_no_app_value(app):
    handler = make_handler('test_app')
    app.router.add_get('/', handler)
    
    client = await web.test_client(app)
    resp = await client.get('/')
    
    assert resp.status == 200
    assert await resp.text() == 'Ok'  # Ensure response is still 'Ok' even without app value