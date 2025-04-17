import logging
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import ServerError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app, caplog):
    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get")

        assert response.status == 200
        assert response.text == "I am get method"
        assert ("sanic.error", logging.INFO, "Handled request") not in caplog.record_tuples

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")

    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_cancelled_error(app, caplog):
    app.config.RESPONSE_TIMEOUT = 1

    @app.middleware("response")
    async def process_response(request, response):
        raise asyncio.CancelledError("CancelledError at response middleware")

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.get("/get")

        assert response.status == 500
        assert ("sanic.error", logging.ERROR, "Exception occurred while handling uri: 'http://127.0.0.1:42101/get'") in caplog.record_tuples