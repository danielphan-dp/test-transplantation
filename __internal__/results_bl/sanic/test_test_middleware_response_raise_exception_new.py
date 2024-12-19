import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_success(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_middleware_exception(app, caplog):
    @app.middleware("response")
    async def process_response(request, response):
        raise Exception("Exception at response middleware")

    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.get("/get")

    assert response.status == 500
    assert (
        "sanic.error",
        logging.ERROR,
        "Exception occurred in one of response middleware handlers",
    ) in caplog.record_tuples

def test_get_method_empty_response(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == ''