import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_error(app):
    @app.get("/error")
    def error_method(request):
        raise Exception("This is an error")

    request, response = app.test_client.get("/error")
    assert response.status == 500
    assert "This is an error" in response.text

def test_get_method_with_custom_content_type(app):
    @app.get("/custom")
    def custom_method(request):
        return text("Custom content", content_type="application/custom")

    request, response = app.test_client.get("/custom")
    assert response.status == 200
    assert response.content_type == "application/custom"