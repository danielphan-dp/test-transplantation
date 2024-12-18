import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404

def test_get_method_invalid_method(app):
    request, response = app.test_client.post("/test")
    assert response.status == 405
    assert "Method POST not allowed for URL /test" in response.text

def test_get_method_with_query_params(app):
    @app.get("/test_with_params")
    def get_method_with_params(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test_with_params?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"