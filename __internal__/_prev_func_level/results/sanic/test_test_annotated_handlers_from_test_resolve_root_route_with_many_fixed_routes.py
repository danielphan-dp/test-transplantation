import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.mark.parametrize("path, expected_response", [
    ("/", "I am get method"),
    ("/test", "I am get method"),
    ("/another_test", "I am get method"),
])
def test_get_method(app, path, expected_response):
    @app.get(path)
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get(path)
    assert response.text == expected_response

@pytest.mark.parametrize("invalid_path", [
    ("/invalid_path"),
    ("/another_invalid_path"),
])
def test_get_method_invalid_path(app, invalid_path):
    @app.get("/valid_path")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get(invalid_path)
    assert response.status == 404
    assert "Requested URL" in response.text