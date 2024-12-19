import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.fixture
def blueprint():
    bp = Blueprint("bp")

    @bp.get("/")
    async def handler(request):
        return text('I am get method')
    
    return bp

@pytest.mark.asyncio
async def test_get_method(app, blueprint):
    app.blueprint(blueprint)
    _, response = await app.test_client.get("/")
    assert response.text == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_with_different_route(app, blueprint):
    @blueprint.get("/different")
    async def different_handler(request):
        return text('I am a different get method')

    app.blueprint(blueprint)
    _, response = await app.test_client.get("/different")
    assert response.text == 'I am a different get method'

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    _, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params(app, blueprint):
    @blueprint.get("/query")
    async def query_handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    app.blueprint(blueprint)
    _, response = await app.test_client.get("/query?param=test")
    assert response.text == "Query param: test"