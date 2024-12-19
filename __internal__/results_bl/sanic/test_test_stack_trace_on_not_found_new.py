import logging
import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/non_existing_endpoint")
    assert response.status == 404

def test_get_method_logging(app, caplog):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/test")

    counter = Counter([(r[0], r[1]) for r in caplog.record_tuples])
    assert response.status == 200
    assert counter[("sanic.root", logging.INFO)] == 1
    assert counter[("sanic.root", logging.ERROR)] == 0
    assert counter[("sanic.error", logging.ERROR)] == 0
    assert counter[("sanic.server", logging.INFO)] == 0

def test_get_method_empty_response(app):
    @app.get("/empty")
    def get_method(request):
        return text('')

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ''