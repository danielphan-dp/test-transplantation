import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.put("/put")
    async def put(request):
        return text("I am put method")

    return app

@pytest.mark.asyncio
async def test_put_method(app):
    request, response = await app.asgi_client.put("/put")
    assert response.status == 200
    assert response.text == "I am put method"

@pytest.mark.asyncio
async def test_put_with_data(app):
    data = "Test data"
    request, response = await app.asgi_client.put("/put", data=data)
    assert response.status == 200
    assert response.text == "I am put method"

@pytest.mark.asyncio
async def test_put_empty_body(app):
    request, response = await app.asgi_client.put("/put", data="")
    assert response.status == 200
    assert response.text == "I am put method"

@pytest.mark.asyncio
async def test_put_invalid_data(app):
    request, response = await app.asgi_client.put("/put", data={"invalid": "data"})
    assert response.status == 200
    assert response.text == "I am put method"