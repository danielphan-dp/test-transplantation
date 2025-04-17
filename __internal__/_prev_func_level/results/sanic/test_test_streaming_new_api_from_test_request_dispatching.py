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

def test_post_with_data(app):
    @app.post("/post_with_data")
    async def post_handler(request):
        return text(request.body.decode())

    request, response = app.test_client.post("/post_with_data", data="Hello")
    assert response.status == 200
    assert response.text == 'Hello'

def test_post_empty_body(app):
    @app.post("/post_empty")
    async def post_handler(request):
        return text('Received empty body' if not request.body else 'Received body')

    request, response = app.test_client.post("/post_empty", data="")
    assert response.status == 200
    assert response.text == 'Received empty body'

def test_post_invalid_method(app):
    @app.post("/post_invalid")
    async def post_handler(request):
        return text('This should not be reached')

    request, response = app.test_client.get("/post_invalid")
    assert response.status == 405
    assert "Method GET not allowed for URL /post_invalid" in response.text

def test_post_with_large_data(app):
    @app.post("/post_large")
    async def post_handler(request):
        return text(f'Received {len(request.body)} bytes')

    large_data = 'x' * 10000
    request, response = app.test_client.post("/post_large", data=large_data)
    assert response.status == 200
    assert response.text == 'Received 10000 bytes'