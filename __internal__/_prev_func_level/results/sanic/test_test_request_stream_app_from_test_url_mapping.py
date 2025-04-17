import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/post")
    async def post(request):
        return text('I am post method')

    return app

@pytest.mark.asyncio
async def test_post_method(app):
    request, response = await app.test_client.post("/post")
    assert response.status == 200
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_with_data(app):
    data = "sample data"
    request, response = await app.test_client.post("/post", data=data)
    assert response.status == 200
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_empty_body(app):
    request, response = await app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_invalid_route(app):
    request, response = await app.test_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.asyncio
async def test_post_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = await app.test_client.post("/post", headers=headers)
    assert response.status == 200
    assert response.text == "I am post method"