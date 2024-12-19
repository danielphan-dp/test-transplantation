import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test_get")
    async def test_get(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/non_existent_route")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_param(app):
    @app.get("/test_get_with_param")
    async def test_get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = await app.test_client.get("/test_get_with_param?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

@pytest.mark.asyncio
async def test_get_method_with_empty_query_param(app):
    request, response = await app.test_client.get("/test_get_with_param?param=")
    assert response.status == 200
    assert response.text == "Received param: "