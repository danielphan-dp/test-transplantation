import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test-get")
    async def get_method(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/test-get")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_with_invalid_route(app):
    request, response = await app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_custom_header(app):
    request, response = await app.test_client.get("/test-get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers.get("Custom-Header") is None  # Custom headers should not affect response

@pytest.mark.asyncio
async def test_get_method_with_query_param(app):
    request, response = await app.test_client.get("/test-get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Ensure query params do not affect response

@pytest.mark.asyncio
async def test_get_method_multiple_requests(app):
    request1, response1 = await app.test_client.get("/test-get")
    request2, response2 = await app.test_client.get("/test-get")
    assert response1.status == 200
    assert response2.status == 200
    assert response1.text == response2.text == "I am get method"