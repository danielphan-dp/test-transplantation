import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method(app):
    @app.post("/post")
    async def post(request):
        return text('I am post method')

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_with_data(app):
    @app.post("/post/data")
    async def post_with_data(request):
        return text(request.json.get("key", ""))

    request, response = app.test_client.post("/post/data", json={"key": "value"})
    assert response.status == 200
    assert response.text == "value"

def test_post_empty_body(app):
    @app.post("/post/empty")
    async def post_empty(request):
        return text("Empty body received")

    request, response = app.test_client.post("/post/empty", data="")
    assert response.status == 200
    assert response.text == "Empty body received"

def test_post_invalid_route(app):
    @app.post("/post/valid")
    async def post_valid(request):
        return text("Valid post")

    request, response = app.test_client.post("/post/invalid")
    assert response.status == 404
    assert "Requested URL /post/invalid not found" in response.text

def test_post_method_with_stream(app):
    @app.post("/post/stream", stream=True)
    async def post_stream(request):
        result = ""
        while True:
            body = await request.stream.read()
            if body is None:
                break
            result += body.decode("utf-8")
        return text(result)

    request, response = app.test_client.post("/post/stream", data="streaming data")
    assert response.status == 200
    assert response.text == "streaming data"