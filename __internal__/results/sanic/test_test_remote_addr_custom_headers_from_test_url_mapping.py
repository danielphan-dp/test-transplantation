import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_custom_header(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    headers = {"X-Custom-Header": "CustomValue"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_method_not_allowed(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

def test_get_method_with_empty_request(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", data="")
    assert response.text == 'I am get method'
    assert response.status == 200