import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.body == b"I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_header(app):
    headers = {"Custom-Header": "TestValue"}
    request, response = app.test_client.get("/", headers=headers)
    assert response.status == 200
    assert response.body == b"I am get method"

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/")
    assert request.method == "GET"
    assert request.path == "/"
    assert response.body == b"I am get method"