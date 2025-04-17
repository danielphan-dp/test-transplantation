import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/post/", strict_slashes=True)
    async def post_handler(request):
        return text("I am post method")

    return app

def test_post_method_success(app):
    request, response = app.test_client.post("/post/")
    assert response.text == "I am post method"

def test_post_method_strict_slash(app):
    request, response = app.test_client.post("/post")
    assert response.status == 404

def test_post_method_with_data(app):
    request, response = app.test_client.post("/post/", json={"key": "value"})
    assert response.text == "I am post method"

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/post/", data="")
    assert response.text == "I am post method"

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid/")
    assert response.status == 404

def test_post_method_with_headers(app):
    headers = {"Content-Type": "application/json"}
    request, response = app.test_client.post("/post/", headers=headers)
    assert response.text == "I am post method"