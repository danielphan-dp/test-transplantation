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
async def test_post_method(client):
    response = await client.post("/post")
    assert response.status == 200
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_with_invalid_route(client):
    response = await client.post("/invalid")
    assert response.status == 404

@pytest.mark.asyncio
async def test_post_method_with_options(client):
    response = await client.options("/post")
    assert response.status == 200
    assert "POST" in response.headers.get("Allow")