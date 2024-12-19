import logging
from collections import Counter
import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app, caplog):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/")

    counter = Counter([(r[0], r[1]) for r in caplog.record_tuples])

    assert response.status == 200
    assert response.text == "I am get method"
    assert counter[("sanic.root", logging.INFO)] == 1
    assert counter[("sanic.root", logging.ERROR)] == 0
    assert counter[("sanic.error", logging.ERROR)] == 0
    assert counter[("sanic.server", logging.INFO)] == 1

def test_get_method_with_invalid_route(app, caplog):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/invalid_route")

    counter = Counter([(r[0], r[1]) for r in caplog.record_tuples])

    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text
    assert counter[("sanic.root", logging.INFO)] == 1
    assert counter[("sanic.root", logging.ERROR)] == 0
    assert counter[("sanic.error", logging.ERROR)] == 0
    assert counter[("sanic.server", logging.INFO)] == 1

def test_get_method_with_logging(app, caplog):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/")

    assert response.status == 200
    assert response.text == "I am get method"
    assert "GET /" in caplog.text
    assert counter[("sanic.root", logging.INFO)] == 1
    assert counter[("sanic.root", logging.ERROR)] == 0
    assert counter[("sanic.error", logging.ERROR)] == 0
    assert counter[("sanic.server", logging.INFO)] == 1