import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text("I am get method")

    return app

@pytest.mark.parametrize("path, expected_response", [
    ("/", "I am get method"),
    ("/nonexistent", "Not Found"),
])
def test_get_method(app, path, expected_response):
    request, response = app.test_client.get(path)
    if path == "/":
        assert response.text == expected_response
    else:
        assert response.status == 404
        assert "Not Found" in response.text

def test_get_method_with_invalid_path(app):
    request, response = app.test_client.get("/invalid_path")
    assert response.status == 404
    assert "Not Found" in response.text

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?foo=bar")
    assert response.text == "I am get method"
    assert response.status == 200