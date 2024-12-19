import logging
import sys
import uuid
import importlib.reload
import io.StringIO
from unittest.mock import ANY, Mock
import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method(monkeypatch):
    app = Sanic("test_get_method")

    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(monkeypatch):
    app = Sanic("test_get_method_invalid")

    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid_route")
    
    assert response.status == 404

def test_get_method_with_query_params(monkeypatch):
    app = Sanic("test_get_method_query")

    @app.route("/get")
    async def get_handler(request):
        return text(f'I am get method with query: {request.args}')

    request, response = app.test_client.get("/get?param=value")
    
    assert response.status == 200
    assert response.text == 'I am get method with query: ImmutableMultiDict([(\'param\', [\'value\'])])'