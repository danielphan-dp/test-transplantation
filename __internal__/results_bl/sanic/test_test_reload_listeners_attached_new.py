import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.mark.asyncio
async def test_get_method(app):
    @app.get("/")
    async def get_method(request):
        return text('I am get method')

    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    @app.get("/notfound")
    async def get_method(request):
        return text('I am get method')

    request, response = await app.test_client.get("/unknown")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    @app.get("/query")
    async def get_method(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = await app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == 'Query param: test'