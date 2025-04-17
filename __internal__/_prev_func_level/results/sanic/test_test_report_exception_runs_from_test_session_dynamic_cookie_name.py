import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_with_exception(app):
    event = asyncio.Event()

    @app.report_exception
    async def catch_any_exception(app: Sanic, exception: Exception):
        event.set()

    @app.route("/error")
    async def error_handler(request):
        1 / 0

    app.test_client.get("/error")
    assert event.is_set()