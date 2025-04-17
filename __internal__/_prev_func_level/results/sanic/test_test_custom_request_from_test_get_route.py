import json
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    return Sanic(name="Test")

@pytest.mark.asyncio
async def test_get_method(app):
    @app.route("/get")
    async def get_handler(request):
        return text("I am get method")

    request, response = await app.test_client.get("/get")

    assert request.body == b""
    assert response.text == "I am get method"
    assert response.status == 200

@pytest.mark.asyncio
async def test_get_method_with_invalid_route(app):
    request, response = await app.test_client.get("/invalid")

    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_custom_headers(app):
    @app.route("/get")
    async def get_handler(request):
        return text("I am get method")

    headers = {"Custom-Header": "Value"}
    request, response = await app.test_client.get("/get", headers=headers)

    assert request.headers.get("Custom-Header") == "Value"
    assert response.text == "I am get method"
    assert response.status == 200

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    @app.route("/get")
    async def get_handler(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = await app.test_client.get("/get?param=test")

    assert request.body == b""
    assert response.text == "Query param: test"
    assert response.status == 200