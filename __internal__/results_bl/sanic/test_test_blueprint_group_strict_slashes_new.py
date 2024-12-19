import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic(name="test-app")
    bp = Blueprint(name="test_bp")

    @bp.get("/test")
    async def test_get(request):
        return text('I am get method')

    app.blueprint(bp)
    return app

@pytest.mark.asyncio
async def test_get_method_status(app):
    request, response = await app.test_client.get("/test")
    assert response.status == 200
    assert response.body == b'I am get method'

@pytest.mark.asyncio
async def test_get_method_invalid_route(app):
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    request, response = await app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.body == b'I am get method'