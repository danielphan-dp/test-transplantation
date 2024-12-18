import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "TestValue"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", data="")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method"
    assert response.status == 200