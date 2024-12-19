import asyncio
import pytest
from threading import Event
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get")
async def get_method(request):
    return text('I am get method')

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.body == b'I am get method'

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", headers={})
    assert response.body == b'I am get method'

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.body == b'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_concurrent_requests(app):
    async def make_request():
        request, response = app.test_client.get("/get")
        return response.body

    tasks = [make_request() for _ in range(10)]
    responses = asyncio.run(asyncio.gather(*tasks))
    assert all(response == b'I am get method' for response in responses)