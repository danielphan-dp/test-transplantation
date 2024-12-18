import asyncio
import pytest
from sanic import Sanic, text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/")
    async def handler(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_param(app):
    @app.route("/greet")
    async def greet(request):
        name = request.args.get("name", "World")
        return text(f"Hello, {name}!")

    request, response = await app.test_client.get("/greet?name=Alice")
    assert response.status == 200
    assert response.text == "Hello, Alice!"