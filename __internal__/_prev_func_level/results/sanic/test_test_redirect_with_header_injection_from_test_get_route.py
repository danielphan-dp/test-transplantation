import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_method")
    async def get_method(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method_status(app):
    request, response = await app.test_client.get("/get_method")
    assert response.status == 200

@pytest.mark.asyncio
async def test_get_method_response_text(app):
    request, response = await app.test_client.get("/get_method")
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_content_type(app):
    request, response = await app.test_client.get("/get_method")
    assert response.content_type == "text/plain; charset=utf-8"

@pytest.mark.asyncio
async def test_get_method_invalid_route(app):
    request, response = await app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text