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

def test_get_method_response(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/")

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_logging(app):
    log_stream = StringIO()
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG, stream=log_stream)
    log = logging.getLogger()
    rand_string = str(uuid.uuid4())

    class DummyView:
        def get(self, request):
            log.info(rand_string)
            return text('I am get method')

    app.add_route(DummyView().get, "/")

    request, response = app.test_client.get("/")
    log_text = log_stream.getvalue()
    assert rand_string in log_text

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    class DummyView:
        def get(self, request):
            return text(f"Query param: {request.args.get('param')}")

    app.add_route(DummyView().get, "/")

    request, response = app.test_client.get("/?param=test")
    assert response.text == "Query param: test"