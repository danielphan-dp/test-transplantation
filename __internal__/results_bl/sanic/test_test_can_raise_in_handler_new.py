import asyncio
from sanic import Sanic, Request, json
from sanic.response import text
import pytest

app = Sanic("TestApp")

@app.get("/test")
async def get_method(request: Request):
    return text('I am get method')

def test_get_method_success(app: Sanic):
    _, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app: Sanic):
    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app: Sanic):
    _, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_cancelled_error(app: Sanic):
    @app.get("/cancel")
    async def handler(request: Request):
        raise asyncio.CancelledError("Request was cancelled")

    @app.exception(asyncio.CancelledError)
    async def handle_cancel(request: Request, exc: asyncio.CancelledError):
        return json({"message": exc.args[0]}, status=418)

    _, response = app.test_client.get("/cancel")
    assert response.status == 418
    assert response.json["message"] == "Request was cancelled"