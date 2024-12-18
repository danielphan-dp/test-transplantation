import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/test_post")
    async def post_method(request):
        return text("I am post method")

    request, response = app.test_client.post("/test_post")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_data(app):
    @app.post("/test_post_data")
    async def post_method_with_data(request):
        data = request.json
        return text(f"Received: {data}")

    request, response = app.test_client.post("/test_post_data", json={"key": "value"})
    assert response.status == 200
    assert response.text == "Received: {'key': 'value'}"

def test_post_method_empty_body(app):
    @app.post("/test_post_empty")
    async def post_method_empty(request):
        return text("Empty body received")

    request, response = app.test_client.post("/test_post_empty", data={})
    assert response.status == 200
    assert response.text == "Empty body received"

def test_post_method_invalid_route(app):
    @app.post("/valid_route")
    async def valid_route(request):
        return text("This is a valid route")

    request, response = app.test_client.post("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_post_method_with_headers(app):
    @app.post("/test_post_headers")
    async def post_method_with_headers(request):
        return text(f"Headers: {request.headers}")

    headers = {"Custom-Header": "Value"}
    request, response = app.test_client.post("/test_post_headers", headers=headers)
    assert response.status == 200
    assert "Custom-Header" in response.text
    assert "Value" in response.text