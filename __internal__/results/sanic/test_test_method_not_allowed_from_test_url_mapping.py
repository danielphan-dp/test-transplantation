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
async def test_post_method(app):
    request, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_not_allowed(app):
    request, response = app.test_client.get("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"POST"}
    assert response.headers["Content-Length"] == "0"

@pytest.mark.asyncio
async def test_post_method_with_invalid_data(app):
    request, response = app.test_client.post("/", data="invalid_data")
    assert response.status == 200
    assert response.text == 'I am post method'  # Ensure it still responds correctly

@pytest.mark.asyncio
async def test_post_method_with_empty_body(app):
    request, response = app.test_client.post("/", data="")
    assert response.status == 200
    assert response.text == 'I am post method'  # Ensure it still responds correctly

@pytest.mark.asyncio
async def test_post_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.post("/", headers=headers)
    assert response.status == 200
    assert response.text == 'I am post method'  # Ensure it still responds correctly