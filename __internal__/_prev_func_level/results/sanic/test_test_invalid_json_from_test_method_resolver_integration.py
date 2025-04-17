import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.post("/")
async def handler(request):
    return text('I am post method')

@pytest.mark.asyncio
async def test_post_method(app):
    request, response = await app.test_client.post("/")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_with_invalid_data(app):
    data = "I am not json"
    request, response = await app.test_client.post("/", data=data)
    assert response.status == 400

@pytest.mark.asyncio
async def test_post_with_empty_body(app):
    request, response = await app.test_client.post("/", data="")
    assert response.status == 400

@pytest.mark.asyncio
async def test_post_with_non_text_data(app):
    request, response = await app.test_client.post("/", data=b'\x00\x01\x02')
    assert response.status == 400

@pytest.mark.asyncio
async def test_post_with_json_data(app):
    request, response = await app.test_client.post("/", json={"key": "value"})
    assert response.status == 200
    assert response.text == 'I am post method'