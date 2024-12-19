import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/1")
    async def get_method(request):
        return text('I am get method')
    return app

@pytest.mark.asyncio
async def test_get_method_success(app):
    request, response = await app.test_client.get("/1")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    request, response = await app.test_client.get("/1?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_timeout(response_timeout_app):
    request, response = response_timeout_app.test_client.get("/1")
    assert response.status == 503
    assert response.text == "Response Timeout from error_handler."