import logging
import uuid
from io import StringIO
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    log_stream = StringIO()
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG, stream=log_stream)
    log = logging.getLogger()

    @app.route("/get")
    def get_method(request):
        log.info("Accessing GET method")
        return text("I am get method")

    request, response = app.test_client.get("/get")
    log_text = log_stream.getvalue()
    
    assert response.text == "I am get method"
    assert "Accessing GET method" in log_text

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    @app.route("/get_with_param")
    def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Received param: test"

def test_get_method_without_query_param(app):
    @app.route("/get_with_param")
    def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param")
    assert response.text == "Received param: default"