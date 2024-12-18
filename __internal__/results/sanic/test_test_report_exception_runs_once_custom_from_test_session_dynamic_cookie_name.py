import asyncio
from itertools import count
import pytest
from sanic import Sanic, text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_event(app):
    event = asyncio.Event()
    c = count()

    @app.report_exception
    async def catch_any_exception(app: Sanic, exception: Exception):
        event.set()
        next(c)

    @app.route("/error")
    async def error_handler(request):
        raise Exception("Test Exception")

    app.test_client.get("/error")

    assert event.is_set()
    assert next(c) == 1