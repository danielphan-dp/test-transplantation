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
    test_client = SanicTestClient(app, port=None)
    request, response = test_client.post("/post")
    assert response.text == "I am post method"
    assert response.status == 200

def test_post_method_invalid_route(app):
    test_client = SanicTestClient(app, port=None)
    request, response = test_client.post("/invalid")
    assert response.status == 404

def test_post_method_with_get(app):
    test_client = SanicTestClient(app, port=None)
    request, response = test_client.get("/post")
    assert response.status == 405

def test_post_method_no_body(app):
    test_client = SanicTestClient(app, port=None)
    request, response = test_client.post("/post", body=None)
    assert response.text == "I am post method"
    assert response.status == 200

def test_post_method_with_headers(app):
    test_client = SanicTestClient(app, port=None)
    headers = {'Content-Type': 'application/json'}
    request, response = test_client.post("/post", headers=headers)
    assert response.text == "I am post method"
    assert response.status == 200