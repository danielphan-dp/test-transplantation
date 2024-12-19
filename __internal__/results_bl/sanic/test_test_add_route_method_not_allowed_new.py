import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/post_test")
    async def post_handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/post_test")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_not_allowed(app):
    @app.get("/post_test")
    async def get_handler(request):
        return text("OK")

    request, response = app.test_client.get("/post_test")
    assert response.status == 200

    request, response = app.test_client.post("/post_test")
    assert response.status == 405

def test_post_method_with_invalid_route(app):
    request, response = app.test_client.post("/invalid_route")
    assert response.status == 404

def test_post_method_with_empty_body(app):
    @app.post("/empty_body")
    async def empty_body_handler(request):
        return text("Received empty body")

    request, response = app.test_client.post("/empty_body", data="")
    assert response.status == 200
    assert response.text == "Received empty body"