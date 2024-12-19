import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/post/", strict_slashes=True)
    def handler(request):
        return text("I am post method")

    return app

def test_post_method_valid(app):
    request, response = app.test_client.post("/post/")
    assert response.text == "I am post method"

def test_post_method_invalid(app):
    request, response = app.test_client.post("/post")
    assert response.status == 404

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/post/", data="")
    assert response.text == "I am post method"

def test_post_method_with_json(app):
    request, response = app.test_client.post("/post/", json={"key": "value"})
    assert response.text == "I am post method"

def test_post_method_with_query_params(app):
    request, response = app.test_client.post("/post/?param=value")
    assert response.text == "I am post method"