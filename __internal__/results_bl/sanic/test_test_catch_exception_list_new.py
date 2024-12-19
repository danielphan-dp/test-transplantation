import logging
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import NotFound, SanicException

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_exception_handling(app):
    @app.exception(SanicException)
    def handle_exception(request, exception):
        return text("Handled exception")

    @app.route("/exception")
    def raise_exception(request):
        raise SanicException("This is a test exception")

    request, response = app.test_client.get("/exception")
    assert response.text == "Handled exception"