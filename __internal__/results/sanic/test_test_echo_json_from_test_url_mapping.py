import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/post")
    async def handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/post")
    
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_data(app):
    @app.post("/post")
    async def handler(request):
        return text(f"Received: {request.json}")

    data = {"key": "value"}
    request, response = app.test_client.post("/post", json=data)

    assert response.status == 200
    assert response.text == 'Received: {"key": "value"}'

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid")

    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_method_method_not_allowed(app):
    @app.post("/post")
    async def handler(request):
        return text('I am post method')

    request, response = app.test_client.get("/post")

    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text