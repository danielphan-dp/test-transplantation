import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_returns_correct_response(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_concurrent_requests(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    async def make_request():
        request, response = app.test_client.get("/get")
        return response.text

    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(make_request()) for _ in range(10)]
    responses = loop.run_until_complete(asyncio.gather(*tasks))

    assert all(response == 'I am get method' for response in responses)