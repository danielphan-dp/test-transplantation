import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text, json
from sanic.request import Request

def test_get_method(app: Sanic):
    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app: Sanic):
    _, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_header(app: Sanic):
    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == 'I am get method'