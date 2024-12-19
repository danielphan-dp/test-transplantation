import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/")
    async def test_get(request):
        return text('I am get method')
    return app

@pytest.mark.asyncio
async def test_get_method_response(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.body.decode() == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_headers(app):
    request, response = await app.test_client.get("/")
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
    assert "Transfer-Encoding" not in response.headers
    assert "Content-Length" in response.headers

@pytest.mark.asyncio
async def test_get_method_empty_request(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    request, response = await app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.body.decode() == 'I am get method'