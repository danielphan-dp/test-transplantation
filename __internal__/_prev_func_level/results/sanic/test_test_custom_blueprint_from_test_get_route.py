import pytest
from sanic import Sanic, text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request: Request):
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
    @app.get("/query")
    async def get_with_query(request: Request):
        param = request.args.get("param", "default")
        return text(f"Query param is {param}")

    request, response = await app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == "Query param is test"

@pytest.mark.asyncio
async def test_get_method_with_empty_query_param(app):
    @app.get("/query")
    async def get_with_query(request: Request):
        param = request.args.get("param", "default")
        return text(f"Query param is {param}")

    request, response = await app.test_client.get("/query")
    assert response.status == 200
    assert response.text == "Query param is default"