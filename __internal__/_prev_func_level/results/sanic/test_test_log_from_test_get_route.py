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
    @app.route("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_logging(app):
    log_stream = StringIO()
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG, stream=log_stream)
    log = logging.getLogger()
    rand_string = str(uuid.uuid4())

    @app.route("/")
    def handler(request):
        log.info(rand_string)
        return text("I am get method")

    request, response = app.test_client.get("/")
    log_text = log_stream.getvalue()
    assert response.status == 200
    assert "I am get method" in response.text
    assert rand_string in log_text

def test_get_method_with_query_param(app):
    @app.route("/<name>")
    def handler(request, name):
        return text(f"Hello, {name}")

    request, response = app.test_client.get("/John")
    assert response.status == 200
    assert response.text == "Hello, John"

def test_get_method_not_found(app):
    @app.route("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_custom_header(app):
    @app.route("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers.get("X-Custom-Header") is None  # Custom header should not be in response