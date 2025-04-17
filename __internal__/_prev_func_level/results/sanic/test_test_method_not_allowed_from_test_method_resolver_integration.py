import pytest
from sanic import Sanic, response
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.post("/")
    async def post_method(request: Request):
        return response.text('I am post method')

    return app

@pytest.mark.asyncio
async def test_post_method_success(app):
    request, response = await app.test_client.post("/")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_not_allowed(app):
    request, response = await app.test_client.get("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"POST"}
    assert response.headers["Content-Length"] == "0"

@pytest.mark.asyncio
async def test_post_method_with_data(app):
    request, response = await app.test_client.post("/", json={"key": "value"})
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_empty_body(app):
    request, response = await app.test_client.post("/", data="")
    assert response.status == 200
    assert response.text == 'I am post method'