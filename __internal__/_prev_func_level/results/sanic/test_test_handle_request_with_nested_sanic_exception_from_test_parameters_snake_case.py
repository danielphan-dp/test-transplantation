import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/test-get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test-get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_error_logging(app, caplog):
    @app.get("/error")
    def handler(request):
        raise Exception("Test Exception")

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.get("/error")
    
    assert response.status == 500
    assert "Test Exception" in response.text
    assert (
        "sanic.error",
        logging.ERROR,
        "Exception occurred while handling uri: 'http://127.0.0.1:80/error'",
    ) in caplog.record_tuples

def test_get_method_with_query_params(app):
    @app.get("/test-get-query")
    def handler(request):
        return text(f"Query param received: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/test-get-query?param=test")
    assert response.status == 200
    assert response.text == "Query param received: test"