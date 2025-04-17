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
        return text("I am post method")

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_data(app):
    @app.post("/post/data")
    async def post_handler(request):
        return text(request.json)

    request, response = app.test_client.post("/post/data", json={"key": "value"})
    assert response.status == 200
    assert response.text == '{"key": "value"}'

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid")
    assert response.status == 404

def test_post_method_with_empty_body(app):
    @app.post("/post/empty")
    async def post_handler(request):
        return text("Empty body received")

    request, response = app.test_client.post("/post/empty", data="")
    assert response.status == 200
    assert response.text == "Empty body received"