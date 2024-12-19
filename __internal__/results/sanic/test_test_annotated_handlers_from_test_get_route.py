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

@pytest.mark.parametrize("path, expected_text", [
    ("/", "I am get method"),
    ("/nonexistent", "Not Found"),
])
def test_get_method(app, path, expected_text):
    request, response = app.test_client.get(path)
    if path == "/":
        assert response.text == expected_text
    else:
        assert response.status == 404
        assert "Not Found" in response.text

@pytest.mark.parametrize("path", [
    ("/"),
])
def test_get_method_status_code(app, path):
    request, response = app.test_client.get(path)
    assert response.status == 200

@pytest.mark.parametrize("path", [
    ("/"),
])
def test_get_method_content_type(app, path):
    request, response = app.test_client.get(path)
    assert response.content_type == "text/plain; charset=utf-8"