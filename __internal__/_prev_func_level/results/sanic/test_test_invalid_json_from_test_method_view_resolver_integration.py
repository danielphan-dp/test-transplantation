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
async def test_post_method_success(app):
    request, response = await app.asgi_client.post("/")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_invalid_data(app):
    data = "Invalid data"
    request, response = await app.asgi_client.post("/", data=data)
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_empty_body(app):
    request, response = await app.asgi_client.post("/", data="")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_json_content_type(app):
    headers = {"Content-Type": "application/json"}
    request, response = await app.asgi_client.post("/", json={"key": "value"}, headers=headers)
    assert response.status == 200
    assert response.text == 'I am post method'