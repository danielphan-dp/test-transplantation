import asyncio
from sanic import Sanic, Request, json, text
import pytest

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request: Request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming the handler does not change based on params

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming the handler does not change based on headers

def test_get_method_with_cancelled_error(app):
    @app.get("/cancel")
    async def cancel_handler(request: Request):
        raise asyncio.CancelledError("STOP!!")

    @app.exception(asyncio.CancelledError)
    async def handle_cancel(request: Request, exc: asyncio.CancelledError):
        return json({"message": exc.args[0]}, status=418)

    request, response = app.test_client.get("/cancel")
    assert response.status == 418
    assert response.json["message"] == "STOP!!"