import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_method(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    request, response = await app.test_client.get("/get?foo=bar")
    assert response.status == 200
    assert response.text == "I am get method"  # Ensure query params do not affect response

@pytest.mark.asyncio
async def test_get_method_with_headers(app):
    request, response = await app.test_client.get("/get", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"  # Ensure headers do not affect response