import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_invalid_route(app):
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    request, response = await app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the method does not change behavior with params

@pytest.mark.asyncio
async def test_get_method_with_headers(app):
    request, response = await app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the method does not change behavior with headers

@pytest.mark.asyncio
async def test_get_method_empty_response(app):
    @app.get("/empty")
    async def empty_method(request):
        return text("")

    request, response = await app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""