import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/")
    async def handler(request):
        return text('I am post method')

    return app

@pytest.mark.asyncio
async def test_post_method(app):
    request, response = await app.asgi_client.post("/")
    
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_with_data(app):
    data = {"key": "value"}
    request, response = await app.asgi_client.post("/", json=data)
    
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_empty_body(app):
    request, response = await app.asgi_client.post("/", json={})
    
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_invalid_json(app):
    request, response = await app.asgi_client.post("/", data="invalid json")
    
    assert response.status == 200
    assert response.text == 'I am post method'