import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method_status(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200

@pytest.mark.asyncio
async def test_get_method_response(app):
    request, response = await app.test_client.get("/")
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_content_type(app):
    request, response = await app.test_client.get("/")
    assert response.content_type == "text/plain; charset=utf-8"