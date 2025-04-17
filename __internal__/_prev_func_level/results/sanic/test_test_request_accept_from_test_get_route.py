import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_with_custom_header(app):
    request, response = await app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert request.headers.get("Custom-Header") == "value"

@pytest.mark.asyncio
async def test_get_method_with_invalid_route(app):
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    request, response = await app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the method does not change based on query params

@pytest.mark.asyncio
async def test_get_method_with_different_accept_header(app):
    header_value = "application/json"
    request, response = await app.test_client.get("/", headers={"Accept": header_value})
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the method does not change based on Accept header