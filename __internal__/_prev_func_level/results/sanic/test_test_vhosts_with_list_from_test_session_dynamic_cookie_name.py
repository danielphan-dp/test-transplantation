import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    headers = {"Custom-Header": "Test"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == 'I am get method'  # Ensure custom headers do not affect response

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'  # Ensure query params do not affect response

def test_get_method_with_different_http_methods(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405  # Ensure POST method is not allowed
    assert "Method POST not allowed for URL /get" in response.text