import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/")
    async def test_get(request):
        return text("I am get method")
    return app

@pytest.mark.asyncio
async def test_get_method_returns_correct_content(app):
    request, response = await app.test_client.get("/")
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_empty_request(app):
    request, response = await app.test_client.get("/?query=")
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_invalid_route(app):
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_headers(app):
    request, response = await app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"