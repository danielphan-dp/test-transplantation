import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

def test_get_method(app: Sanic):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app: Sanic):
    request, response = app.test_client.get("/invalid")

    assert response.status == 404

def test_get_method_with_query_params(app: Sanic):
    @app.route("/get")
    async def get_handler(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/get?param=test")

    assert response.status == 200
    assert response.text == 'Query param: test'

def test_get_method_with_no_query_params(app: Sanic):
    @app.route("/get")
    async def get_handler(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == 'Query param: none'