import logging
import pytest
from itertools import count
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_success(app):
    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    _, response = app.test_client.get("/not-found")
    assert response.status == 404

def test_request_middleware_exception_on_get(app: Sanic):
    counter = count()

    @app.on_request
    def request_middleware(request):
        next(counter)
        raise Exception

    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.status == 500
    assert next(counter) == 1