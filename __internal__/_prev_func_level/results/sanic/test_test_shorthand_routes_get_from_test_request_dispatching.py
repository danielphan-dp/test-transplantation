import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/post")
    def post_handler(request):
        return text("I am post method")

    return app

def test_post_method_success(app):
    request, response = app.test_client.post("/post")
    assert response.text == "I am post method"

def test_post_method_not_allowed(app):
    request, response = app.test_client.get("/post")
    assert response.status == 405

def test_post_method_with_invalid_route(app):
    request, response = app.test_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_method_with_additional_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.post("/post", headers=headers)
    assert response.text == "I am post method"
    assert request.headers.get("Custom-Header") == "value"