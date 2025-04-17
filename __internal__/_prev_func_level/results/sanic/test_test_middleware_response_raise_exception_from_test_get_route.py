import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.mark.asyncio
async def test_get_method_response(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_with_middleware(app):
    results = []

    @app.middleware("response")
    async def process_response(request, response):
        results.append(response)

    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"
    assert len(results) == 1
    assert isinstance(results[0], type(response))

@pytest.mark.asyncio
async def test_get_method_with_error_logging(app, caplog):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    with caplog.at_level(logging.ERROR):
        request, response = await app.test_client.get("/nonexistent")
    
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text
    assert ("sanic.error", logging.ERROR, "Exception occurred while handling uri: 'http://127.0.0.1:42101/nonexistent'") in caplog.record_tuples

@pytest.mark.asyncio
async def test_get_method_with_custom_error(app):
    @app.get("/error")
    async def handler(request):
        raise Exception("Custom error")

    request, response = await app.test_client.get("/error")
    assert response.status == 500
    assert "Custom error" in response.text