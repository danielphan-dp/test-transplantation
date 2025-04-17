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
async def test_get_method_success(app):
    request, response = await app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_invalid_route(app):
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_ssl(app):
    request, response = await app.test_client.get("/get", server_kwargs={"ssl": True})
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_without_ssl(app):
    with pytest.raises(ValueError) as excinfo:
        await app.test_client.get("/get", server_kwargs={"ssl": False})
    assert "Invalid ssl argument" in str(excinfo.value)