import pytest
from aiohttp import web
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.mark.parametrize('appname, my_value', [
    ('app1', 'value1'),
    ('app2', 'value2'),
    ('', 'value3'),  # Edge case: empty appname
    ('app3', None),  # Edge case: None as my_value
])
async def test_make_handler_valid(appname, my_value):
    values = []
    app = web.Application()
    app[my_value] = 'test_value'
    handler = make_handler(appname)

    request = web.Request(
        method='GET',
        path='/',
        app=app
    )
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert values == [f'{appname}: test_value']

@pytest.mark.parametrize('appname', [
    ('invalid name'),  # Invalid appname
    ('class'),  # Invalid appname
])
async def test_make_handler_invalid(appname):
    with pytest.raises(ValueError):
        handler = make_handler(appname)  # Expecting ValueError on invalid appname usage