import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get-method")
    async def get_method(request: Request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/get-method")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/non-existent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_param(app):
    @app.get("/get-method-with-param")
    async def get_method_with_param(request: Request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = await app.test_client.get("/get-method-with-param?param=test")
    assert response.status == 200
    assert response.text == "I am get method with param: test"