import asyncio
import logging
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_success(app):
    @app.get("/test-get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test-get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_exception(app, monkeypatch, caplog):
    @app.get("/test-get-exception")
    def handler(request):
        raise Exception("Test Exception")

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.get("/test-get-exception")
    port = request.server_port
    assert port > 0
    assert response.status == 500
    assert "Test Exception" in response.text
    assert (
        'sanic.error',
        logging.ERROR,
        f"Exception occurred while handling uri: 'http://127.0.0.1:{port}/test-get-exception'",
    ) in caplog.record_tuples

def test_get_method_with_sanic_exception(app, monkeypatch, caplog):
    def mock_error_handler_response(*args, **kwargs):
        raise SanicException("Mock SanicException")

    monkeypatch.setattr(app.error_handler, "response", mock_error_handler_response)

    @app.get("/test-get-sanic-exception")
    def handler(request):
        raise SanicException("This is a SanicException")

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.get("/test-get-sanic-exception")
    port = request.server_port
    assert port > 0
    assert response.status == 500
    assert "This is a SanicException" in response.text
    assert (
        'sanic.error',
        logging.ERROR,
        f"Exception occurred while handling uri: 'http://127.0.0.1:{port}/test-get-sanic-exception'",
    ) in caplog.record_tuples