import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_data(app):
    @app.post("/post_with_data")
    async def post_handler(request):
        return text(request.body.decode())

    request, response = app.test_client.post("/post_with_data", data="Hello")
    assert response.status == 200
    assert response.text == 'Hello'

def test_post_method_empty_body(app):
    @app.post("/post_empty")
    async def post_handler(request):
        return text('Empty body received')

    request, response = app.test_client.post("/post_empty", data="")
    assert response.status == 200
    assert response.text == 'Empty body received'

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid_route")
    assert response.status == 404

def test_post_method_with_large_data(app):
    @app.post("/post_large_data")
    async def post_handler(request):
        return text(f'Received {len(request.body)} bytes')

    large_data = 'x' * 10000
    request, response = app.test_client.post("/post_large_data", data=large_data)
    assert response.status == 200
    assert response.text == 'Received 10000 bytes'