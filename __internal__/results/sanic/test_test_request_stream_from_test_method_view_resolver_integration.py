import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")

    class PostView(HTTPMethodView):
        def post(self, request):
            return text('I am post method')

    app.add_route(PostView.as_view(), "/post_view")

    return app

@pytest.mark.asyncio
async def test_post_view(app):
    request, response = await app.test_client.post("/post_view")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_view_with_data(app):
    data = "test data"
    request, response = await app.test_client.post("/post_view", data=data)
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_view_empty_data(app):
    request, response = await app.test_client.post("/post_view", data="")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_view_invalid_method(app):
    request, response = await app.test_client.get("/post_view")
    assert response.status == 405
    assert "Method GET not allowed for URL /post_view" in response.text

@pytest.mark.asyncio
async def test_post_view_not_found(app):
    request, response = await app.test_client.post("/invalid_post_view")
    assert response.status == 404
    assert "Requested URL /invalid_post_view not found" in response.text