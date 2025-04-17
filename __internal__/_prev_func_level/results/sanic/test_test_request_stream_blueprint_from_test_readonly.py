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
    request, response = await app.asgi_client.patch("/patch", data="Test Data")
    assert response.status == 200
    assert response.text == "I am patch method"

@pytest.mark.asyncio
async def test_patch_empty_body(app):
    request, response = await app.asgi_client.patch("/patch", data="")
    assert response.status == 200
    assert response.text == "I am patch method"

@pytest.mark.asyncio
async def test_patch_invalid_route(app):
    request, response = await app.asgi_client.patch("/invalid")
    assert response.status == 404

@pytest.mark.asyncio
async def test_patch_with_headers(app):
    request, response = await app.asgi_client.patch("/patch", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am patch method"