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

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid_post")
    assert response.status == 404

def test_post_method_with_data(app):
    request, response = app.test_client.post("/post/", data={"key": "value"})
    assert response.text == "I am post method"  # Assuming the handler does not change based on data

def test_post_method_options(app):
    request, response = app.test_client.options("/post/")
    assert response.status == 200  # Assuming OPTIONS is allowed and returns 200

def test_post_method_head(app):
    request, response = app.test_client.head("/post/")
    assert response.status == 200
    assert not response.text  # HEAD should not return a body