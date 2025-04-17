import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_repr(app):
    request, response = app.test_client.get("/")
    assert repr(request) == "<Request: GET />"

def test_get_method_with_none_method(app):
    request, response = app.test_client.get("/")
    request.method = None
    assert repr(request) == "<Request: None />"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/", headers=headers)
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers["Custom-Header"] == "value"