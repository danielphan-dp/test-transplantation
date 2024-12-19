import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/post")
    def handler(request):
        return text("I am post method")

    return app

def test_post_method(app):
    request, response = app.test_client.post("/post")
    assert response.text == "I am post method"
    assert response.status == 200

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405

def test_post_method_with_invalid_data(app):
    request, response = app.test_client.post("/post", json={"invalid": "data"})
    assert response.text == "I am post method"
    assert response.status == 200

def test_post_method_empty_request(app):
    request, response = app.test_client.post("/post", data="")
    assert response.text == "I am post method"
    assert response.status == 200