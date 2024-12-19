import logging
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    
    assert response.status == 404
    assert response.text == 'Not Found'

def test_get_method_with_middleware(app, caplog):
    @app.middleware("response")
    async def process_response(request, response):
        raise asyncio.CancelledError("CancelledError at response middleware")

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.get("/get")

        assert response.status == 500
        assert (
            "sanic.error",
            logging.ERROR,
            "Exception occurred while handling uri: 'http://127.0.0.1:42101/get'",
        ) not in caplog.record_tuples