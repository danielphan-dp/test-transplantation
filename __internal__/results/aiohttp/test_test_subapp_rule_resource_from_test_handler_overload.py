import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import Domain
from your_module import make_handler  # Adjust the import based on your module structure

@pytest.fixture
def app():
    return web.Application()

@pytest.mark.asyncio
async def test_make_handler(app):
    appname = "test_app"
    my_value = "my_value"
    app[my_value] = "test_value"
    handler = make_handler(appname)

    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == "Ok"

    # Check if the value was appended correctly
    assert f'{appname}: test_value' in values

@pytest.mark.asyncio
async def test_make_handler_no_value(app):
    appname = "test_app"
    my_value = "my_value"
    handler = make_handler(appname)

    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == "Ok"

    # Check if the value was appended correctly when my_value is not set
    assert f'{appname}: None' in values

@pytest.mark.asyncio
async def test_make_handler_invalid_request(app):
    appname = "test_app"
    handler = make_handler(appname)

    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    resp = await client.post("/")  # Invalid method
    assert resp.status == 405  # Method Not Allowed

@pytest.mark.asyncio
async def test_make_handler_multiple_requests(app):
    appname = "test_app"
    my_value = "my_value"
    app[my_value] = "test_value"
    handler = make_handler(appname)

    app.router.add_get("/", handler)
    client = await aiohttp_client(app)

    for _ in range(5):
        resp = await client.get("/")
        assert resp.status == 200
        assert await resp.text() == "Ok"

    # Check if the value was appended correctly multiple times
    assert values.count(f'{appname}: test_value') == 5