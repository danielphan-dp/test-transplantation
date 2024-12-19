import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    bp = Blueprint("test_blueprint")

    @bp.patch("/patch")
    async def patch(request):
        return text("I am patch method")

    app.blueprint(bp)
    return app

@pytest.mark.asyncio
async def test_patch_method(app):
    request, response = await app.asgi_client.patch("/patch")
    assert response.status == 200
    assert response.text == "I am patch method"

@pytest.mark.asyncio
async def test_patch_with_data(app):
    data = "Sample data for patch"
    request, response = await app.asgi_client.patch("/patch", data=data)
    assert response.status == 200
    assert response.text == "I am patch method"

@pytest.mark.asyncio
async def test_patch_empty_body(app):
    request, response = await app.asgi_client.patch("/patch", data="")
    assert response.status == 200
    assert response.text == "I am patch method"

@pytest.mark.asyncio
async def test_patch_invalid_route(app):
    request, response = await app.asgi_client.patch("/invalid_patch")
    assert response.status == 404

@pytest.mark.asyncio
async def test_patch_with_large_data(app):
    large_data = "x" * 10000  # Simulating large payload
    request, response = await app.asgi_client.patch("/patch", data=large_data)
    assert response.status == 200
    assert response.text == "I am patch method"