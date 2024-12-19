import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method_without_slash(app):
    @app.post("/test")
    async def post_method(request):
        return text("I am post method")

    request, response = app.test_client.post("/test")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_slash(app):
    @app.post("/test/")
    async def post_method(request):
        return text("I am post method")

    request, response = app.test_client.post("/test/")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_method_with_payload(app):
    @app.post("/test")
    async def post_method(request):
        return text(request.json.get("key", "I am post method"))

    request, response = app.test_client.post("/test", json={"key": "value"})
    assert response.status == 200
    assert response.text == "value"

def test_post_method_empty_payload(app):
    @app.post("/test")
    async def post_method(request):
        return text("I am post method")

    request, response = app.test_client.post("/test", json={})
    assert response.status == 200
    assert response.text == "I am post method"