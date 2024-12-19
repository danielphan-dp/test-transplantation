import logging
import uuid
from io import StringIO
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get")
    def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_logging(app):
    log_stream = StringIO()
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG, stream=log_stream)
    log = logging.getLogger()
    rand_string = str(uuid.uuid4())

    @app.route("/get_with_log")
    def get_with_log_handler(request):
        log.info(rand_string)
        return text('I am get method with log')

    request, response = app.test_client.get("/get_with_log")
    log_text = log_stream.getvalue()
    assert response.status == 200
    assert response.text == 'I am get method with log'
    assert rand_string in log_text

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404