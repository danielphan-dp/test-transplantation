import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method(app):
    @app.post("/post")
    def handler(request):
        return text("I am post method")

    test_client = SanicTestClient(app, port=None)

    request, response = test_client.post("/post")
    assert response.text == "I am post method"

    request, response = test_client.get("/post")
    assert response.status == 405

def test_post_method_with_invalid_route(app):
    test_client = SanicTestClient(app, port=None)

    request, response = test_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_method_with_empty_body(app):
    @app.post("/post")
    def handler(request):
        return text("I am post method")

    test_client = SanicTestClient(app, port=None)

    request, response = test_client.post("/post", data="")
    assert response.text == "I am post method"