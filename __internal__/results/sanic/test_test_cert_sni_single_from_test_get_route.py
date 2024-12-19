import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_param(app):
    @app.get("/get_with_param")
    def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = await app.test_client.get("/get_with_param?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

@pytest.mark.asyncio
async def test_get_method_empty_response(app):
    @app.get("/empty")
    def empty_response(request):
        return text("")

    request, response = await app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""