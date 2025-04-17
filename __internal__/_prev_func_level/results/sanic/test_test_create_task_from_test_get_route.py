import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/get")
    assert response.status == 200
    assert response.body == b'I am get method'

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404
    assert b"Requested URL /nonexistent not found" in response.body

@pytest.mark.asyncio
async def test_get_method_with_delay(app):
    async def delayed_get(request):
        await asyncio.sleep(0.1)
        return text('I am get method after delay')

    app.add_route(delayed_get, "/delayed_get")

    request, response = await app.test_client.get("/delayed_get")
    assert response.status == 200
    assert response.body == b'I am get method after delay'