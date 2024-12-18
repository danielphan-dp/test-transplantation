import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/post")
    def post_handler(request):
        return text("I am post method")

    return app

def test_post_method_success(app):
    test_client = SanicTestClient(app)

    request, response = test_client.post("/post")
    assert response.text == "I am post method"
    assert response.status == 200

def test_post_method_invalid_route(app):
    test_client = SanicTestClient(app)

    request, response = test_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_method_with_data(app):
    test_client = SanicTestClient(app)

    request, response = test_client.post("/post", data={"key": "value"})
    assert response.text == "I am post method"
    assert response.status == 200

def test_post_method_with_empty_data(app):
    test_client = SanicTestClient(app)

    request, response = test_client.post("/post", data={})
    assert response.text == "I am post method"
    assert response.status == 200

def test_post_method_method_not_allowed(app):
    test_client = SanicTestClient(app)

    request, response = test_client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text