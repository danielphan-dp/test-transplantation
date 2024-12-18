import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")
    return app

@pytest.mark.asyncio
async def test_get_method_response(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_middleware(app):
    results = []

    @app.middleware("request")
    async def middleware(request):
        results.append(request)

    request, response = await app.test_client.get("/")
    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0] is request

@pytest.mark.asyncio
async def test_get_method_multiple_requests(app):
    request1, response1 = await app.test_client.get("/")
    request2, response2 = await app.test_client.get("/")
    
    assert response1.text == "I am get method"
    assert response2.text == "I am get method"
    assert response1.status == 200
    assert response2.status == 200