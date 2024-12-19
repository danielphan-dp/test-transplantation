import logging
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_exception(app):
    @app.get("/")
    def handler(request):
        raise SanicException("Mock SanicException")

    with pytest.raises(SanicException):
        request, response = app.test_client.get("/")
    
def test_get_method_with_logging(app, caplog):
    @app.get("/")
    def handler(request):
        return text('I am get method')

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert "I am get method" in response.text
    assert ("sanic.access", logging.INFO, "GET /") in caplog.record_tuples

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/")
    def handler(request):
        return text('I am get method', headers={'X-Custom-Header': 'value'})

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'value'