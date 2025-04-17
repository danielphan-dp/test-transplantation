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
        return text("I am post method")

    request, response = app.test_client.post("/post")
    assert response.text == "I am post method"

    request, response = app.test_client.get("/post")
    assert response.status == 405

def test_post_method_with_invalid_route(app):
    request, response = app.test_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_method_with_data(app):
    @app.post("/post/data")
    async def handler(request):
        return text(request.json.get("key", "No key found"))

    request, response = app.test_client.post("/post/data", json={"key": "value"})
    assert response.text == "value"

    request, response = app.test_client.post("/post/data", json={})
    assert response.text == "No key found"