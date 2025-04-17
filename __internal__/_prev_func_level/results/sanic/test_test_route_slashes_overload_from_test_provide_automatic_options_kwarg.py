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
    assert response.status == 404  # Assuming no route exists for this path

def test_post_method_invalid_method(app):
    request, response = app.test_client.get("/hello/")
    assert response.status == 405  # Method not allowed

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/hello/", data="")
    assert response.text == "I am post method"  # Check if it still responds correctly

def test_post_method_with_headers(app):
    headers = {"Content-Type": "application/json"}
    request, response = app.test_client.post("/hello/", headers=headers)
    assert response.text == "I am post method"  # Check if it still responds correctly with headers