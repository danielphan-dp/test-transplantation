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

    request, response = app.test_client.post("/post_with_data", data="Hello World")
    assert response.status == 200
    assert response.text == 'Hello World'

def test_post_empty_body(app):
    @app.post("/post_empty")
    async def post_handler(request):
        return text('Empty body received' if not request.body else 'Body received')

    request, response = app.test_client.post("/post_empty", data="")
    assert response.status == 200
    assert response.text == 'Empty body received'

def test_post_invalid_route(app):
    request, response = app.test_client.post("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_post_method_with_headers(app):
    @app.post("/post_with_headers")
    async def post_handler(request):
        return text(request.headers.get('X-Custom-Header', 'No Header'))

    request, response = app.test_client.post("/post_with_headers", headers={'X-Custom-Header': 'TestValue'})
    assert response.status == 200
    assert response.text == 'TestValue'