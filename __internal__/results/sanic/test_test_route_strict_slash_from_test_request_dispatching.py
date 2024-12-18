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

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/post/", data="")
    assert response.text == "I am post method"  # Assuming the handler does not change based on empty body

def test_post_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.post("/post/", headers=headers)
    assert response.text == "I am post method"  # Assuming the handler does not change based on headers