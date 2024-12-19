import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    app.config.KEEP_ALIVE_TIMEOUT = 1

    @app.get("/")
    async def base_handler(request):
        return text("111122223333444455556666777788889999")

    @app.post("/upload", stream=True)
    async def upload_handler(request):
        data = [part.decode("utf-8") async for part in request.stream]
        return json(data)

    @app.post("/test_post")
    async def post_handler(request):
        return text('I am post method')

    return app

@pytest.mark.asyncio
async def test_post_method(client):
    request, response = await client.post('/test_post')
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_data(client):
    request, response = await client.post('/test_post', json={'key': 'value'})
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_empty(client):
    request, response = await client.post('/test_post', json={})
    assert response.status == 200
    assert response.text == 'I am post method'