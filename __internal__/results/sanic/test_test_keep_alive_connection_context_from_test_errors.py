import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    async def test_get_method(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method_response(app):
    request, response = await app.test_client.get("/test")
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"

@pytest.mark.asyncio
async def test_get_method_with_invalid_route(app):
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404
    assert response.headers.get("content-type") == "application/problem+json"

@pytest.mark.asyncio
async def test_get_method_with_custom_header(app):
    request, response = await app.test_client.get("/test", headers={"X-Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("X-Custom-Header") is None

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    request, response = await app.test_client.get("/test?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

@pytest.mark.asyncio
async def test_get_method_with_empty_request(app):
    request, response = await app.test_client.get("/test", data={})
    assert response.text == "I am get method"
    assert response.status == 200