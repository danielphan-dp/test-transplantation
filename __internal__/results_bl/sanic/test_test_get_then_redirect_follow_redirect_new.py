import pytest
from sanic.response import text

@pytest.fixture
def app():
    from sanic import Sanic
    app = Sanic("TestApp")

    @app.get("/test_get")
    async def test_get(request):
        return text('I am get method')

    return app

@pytest.mark.asyncio
async def test_get_method_status(app):
    request, response = await app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_empty_path(app):
    request, response = await app.test_client.get("/")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_invalid_route(app):
    request, response = await app.test_client.get("/invalid_route")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    request, response = await app.test_client.get("/test_get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"