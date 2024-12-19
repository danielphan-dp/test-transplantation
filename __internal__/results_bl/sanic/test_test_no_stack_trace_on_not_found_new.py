import logging
import pytest
from collections import Counter
from sanic import Sanic
from sanic.text import text
from sanic.exceptions import FileNotFound

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.get("/test_get")
    async def test_get(request):
        return text('I am get method')

    request, response = app.test_client.get("/test_get")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    @app.get("/test_get")
    async def test_get(request):
        return text('I am get method')

    request, response = app.test_client.get("/non_existing_route")
    
    assert response.status == 404
    assert response.text == 'Not Found'

def test_get_method_logging(app, caplog):
    @app.get("/test_get")
    async def test_get(request):
        return text('I am get method')

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/test_get")

    counter = Counter([(r[0], r[1]) for r in caplog.record_tuples])

    assert response.status == 200
    assert counter[("sanic.root", logging.INFO)] == 1
    assert counter[("sanic.root", logging.ERROR)] == 0
    assert counter[("sanic.error", logging.ERROR)] == 0
    assert counter[("sanic.server", logging.INFO)] == 1
    assert response.text == 'I am get method'