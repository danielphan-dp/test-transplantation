import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_test")
    async def get_handler(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method_success(app):
    request, response = await app.test_client.get("/get_test")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_ssl(app):
    ssl_list = [None]
    with pytest.raises(ValueError) as excinfo:
        await app.test_client.get("/get_test", server_kwargs={"ssl": ssl_list})
    assert "No certificates" in str(excinfo.value)