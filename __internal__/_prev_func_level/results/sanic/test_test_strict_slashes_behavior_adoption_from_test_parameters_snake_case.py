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

def test_get_method_status_code(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_path(app):
    request, response = app.test_client.get("/get/")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_different_path(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_strict_slashes(app):
    app.strict_slashes = True
    request, response = app.test_client.get("/get/")
    assert response.status == 404

    app.strict_slashes = False
    request, response = app.test_client.get("/get/")
    assert response.status == 200
    assert response.text == "I am get method"