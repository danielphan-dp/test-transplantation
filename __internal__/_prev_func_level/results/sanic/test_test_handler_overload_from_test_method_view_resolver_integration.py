import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/test_post")
    async def post_handler(request):
        return text("I am post method")

    return app

def test_post_method(app):
    request, response = app.test_client.post("/test_post")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_data(app):
    request, response = app.test_client.post("/test_post", json={"key": "value"})
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/test_post", data="")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid_route")
    assert response.status == 404

def test_post_method_with_headers(app):
    headers = {"Content-Type": "application/json"}
    request, response = app.test_client.post("/test_post", headers=headers)
    assert response.status == 200
    assert response.text == "I am post method"