import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize("url, expected_response", [
    ("/", "I am get method"),
    ("/nonexistent", "404 Not Found"),
])
def test_get_method_responses(url, expected_response):
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get(url)

    if url == "/":
        assert response.text == expected_response
    else:
        assert response.status == 404
        assert "Not Found" in response.text

@pytest.mark.parametrize("url, expected_status", [
    ("/", 200),
    ("/invalid", 404),
])
def test_get_method_status_codes(url, expected_status):
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get(url)
    assert response.status == expected_status