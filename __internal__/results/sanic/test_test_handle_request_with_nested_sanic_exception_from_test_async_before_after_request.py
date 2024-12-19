import logging
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get(request):
        return text('I am get method')

    return app

def test_get_method_response(app, caplog):
    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == 'I am get method'
    assert "GET request to /get" in caplog.text

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_exception(app, monkeypatch):
    def mock_get_method(*args, **kwargs):
        raise SanicException("Mock SanicException")

    monkeypatch.setattr(app.get, "get", mock_get_method)

    request, response = app.test_client.get("/get")
    assert response.status == 500
    assert "Mock SanicException" in response.text

def test_get_method_logging(app, caplog):
    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert "GET request to /get" in caplog.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'