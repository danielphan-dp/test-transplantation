import logging
import pytest
from collections import Counter
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_logging(app, caplog):
    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get")

    counter = Counter([(r[0], r[1]) for r in caplog.record_tuples])

    assert response.status == 200
    assert response.text == "I am get method"
    assert counter[("sanic.root", logging.INFO)] == 1
    assert counter[("sanic.root", logging.ERROR)] == 0

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existing_route")
    
    assert response.status == 404
    assert response.text == "Requested URL /non_existing_route not found"