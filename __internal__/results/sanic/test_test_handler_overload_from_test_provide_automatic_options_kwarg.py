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

def test_post_method_with_invalid_route(app):
    request, response = app.test_client.get("/test_post")
    assert response.status == 405
    assert "Method GET not allowed for URL /test_post" in response.text

def test_post_method_with_empty_body(app):
    @app.post("/test_post_empty")
    async def post_method_empty(request):
        return text("I am post method with empty body")

    request, response = app.test_client.post("/test_post_empty", data="")
    assert response.status == 200
    assert response.text == "I am post method with empty body"

def test_post_method_with_json_payload(app):
    @app.post("/test_post_json")
    async def post_method_json(request):
        return text("Received JSON")

    request, response = app.test_client.post("/test_post_json", json={"key": "value"})
    assert response.status == 200
    assert response.text == "Received JSON"