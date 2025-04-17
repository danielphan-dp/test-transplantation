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

@pytest.mark.parametrize("expected", ["I am get method"])
def test_get_method(app, expected):
    request, response = app.test_client.get("/get")
    assert response.text == expected

@pytest.mark.parametrize("invalid_path", ["/invalid", "/nonexistent"])
def test_get_method_invalid_path(app, invalid_path):
    request, response = app.test_client.get(invalid_path)
    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize("method", ["post", "put", "delete"])
def test_get_method_invalid_method(app, method):
    request, response = app.test_client.request(method, "/get")
    assert response.status == 405
    assert "Method" in response.text