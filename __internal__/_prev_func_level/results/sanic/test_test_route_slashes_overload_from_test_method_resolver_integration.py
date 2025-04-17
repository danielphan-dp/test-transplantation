import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/hello/")
    def handler_post(request):
        return text("I am post method")

    return app

def test_post_method(app):
    request, response = app.test_client.post("/hello/")
    assert response.text == "I am post method"

def test_post_method_with_slash(app):
    request, response = app.test_client.post("/hello")
    assert response.text == "I am post method"

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid_route")
    assert response.status == 404

def test_post_method_with_data(app):
    request, response = app.test_client.post("/hello/", json={"key": "value"})
    assert response.text == "I am post method"  # Assuming the handler does not change based on input

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/hello/", data="")
    assert response.text == "I am post method"  # Assuming the handler does not change based on input

def test_post_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.post("/hello/", headers=headers)
    assert response.text == "I am post method"  # Assuming the handler does not change based on headers