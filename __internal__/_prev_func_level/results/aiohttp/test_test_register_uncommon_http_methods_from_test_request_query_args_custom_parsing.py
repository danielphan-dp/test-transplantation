import pytest
from aiohttp import web
from aiohttp.test_utils import AiohttpClient

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.mark.parametrize("appname, expected_value", [
    ("test_app", "test_app: None"),
    ("another_app", "another_app: None"),
])
async def test_make_handler(app: web.Application, appname: str, expected_value: str, aiohttp_client: AiohttpClient):
    my_value = "my_value"
    app[my_value] = None
    handler = make_handler(appname)
    app.router.add_get("/test", handler)

    client = await aiohttp_client(app)
    request = await client.get("/test")
    
    assert request.status == 200
    assert await request.text() == 'Ok'
    assert expected_value in request.app[my_value]  # Check if the value is appended correctly

@pytest.mark.parametrize("method", [
    "PROPFIND", "PROPPATCH", "COPY", "LOCK", "UNLOCK", "MOVE", "SUBSCRIBE", "UNSUBSCRIBE", "NOTIFY"
])
async def test_register_uncommon_http_methods(app: web.Application, method: str, aiohttp_client: AiohttpClient):
    my_value = "my_value"
    app[my_value] = "test_value"
    handler = make_handler("test_app")
    app.router.add_route(method, "/handler/to/path", handler)

    client = await aiohttp_client(app)
    request = await client.request(method, "/handler/to/path")
    
    assert request.status == 200
    assert await request.text() == 'Ok'
    assert f'test_app: test_value' in request.app[my_value]  # Ensure the value is appended correctly