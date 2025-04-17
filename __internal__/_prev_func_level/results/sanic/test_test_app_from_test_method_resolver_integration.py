import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    app.config.KEEP_ALIVE_TIMEOUT = 1

    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    return app

@pytest.mark.asyncio
async def test_post_method(app):
    request, response = await app.asgi_client.post("/post")
    assert response.text == 'I am post method'
    assert response.status == 200

@pytest.mark.asyncio
async def test_post_method_with_data(app):
    request, response = await app.asgi_client.post("/post", json={"key": "value"})
    assert response.text == 'I am post method'
    assert response.status == 200

@pytest.mark.asyncio
async def test_post_method_empty_body(app):
    request, response = await app.asgi_client.post("/post", data="")
    assert response.text == 'I am post method'
    assert response.status == 200

@pytest.mark.asyncio
async def test_post_method_invalid_route(app):
    request, response = await app.asgi_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.asyncio
async def test_post_method_method_not_allowed(app):
    request, response = await app.asgi_client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text