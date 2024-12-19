import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_success(app):
    @app.get("/test")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_error(app, monkeypatch):
    err_msg = "Mock Exception"

    def mock_error_handler_response(*args, **kwargs):
        raise Exception(err_msg)

    monkeypatch.setattr(app.error_handler, "response", mock_error_handler_response)

    @app.get("/error")
    def handler(request):
        raise Exception

    request, response = app.test_client.get("/error")
    assert response.status == 500
    assert response.text == "An error occurred while handling an error"