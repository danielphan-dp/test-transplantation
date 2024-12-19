import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

@pytest.mark.parametrize("path, expected_response", [
    ("/get", "I am get method"),
    ("/nonexistent", "Not Found"),
])
def test_get_method(app, path, expected_response):
    request, response = app.test_client.get(path)
    if path == "/get":
        assert response.text == expected_response
    else:
        assert response.status == 404
        assert "Not Found" in response.text

def test_get_method_invalid_request(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text