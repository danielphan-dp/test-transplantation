import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import ReusableClient

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/post")
    async def post_method(request):
        return text("I am post method")

    return app

@pytest.mark.asyncio
async def test_post_method_response(app):
    async with ReusableClient(app) as client:
        request, response = await client.post("/post")
        assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_empty_body(app):
    async with ReusableClient(app) as client:
        request, response = await client.post("/post", data="")
        assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_with_headers(app):
    async with ReusableClient(app) as client:
        headers = {"Custom-Header": "Test"}
        request, response = await client.post("/post", headers=headers)
        assert response.text == "I am post method"
        assert request.headers["Custom-Header"] == "Test"

@pytest.mark.asyncio
async def test_post_method_invalid_route(app):
    async with ReusableClient(app) as client:
        request, response = await client.post("/invalid")
        assert response.status == 404

@pytest.mark.asyncio
async def test_post_method_with_query_params(app):
    async with ReusableClient(app) as client:
        request, response = await client.post("/post?param=value")
        assert response.text == "I am post method"