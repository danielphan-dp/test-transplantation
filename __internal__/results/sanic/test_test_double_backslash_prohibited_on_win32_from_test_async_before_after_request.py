import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.asyncio
async def test_get_method_response():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = await app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_invalid_route():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = await app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_query_param():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text(f'I am get method with param: {request.args.get("param", "None")}')

    request, response = await app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'I am get method with param: test'