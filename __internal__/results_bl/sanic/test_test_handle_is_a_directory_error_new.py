import logging
import os
import sys
import collections
from pathlib import Path
import time
from time import gmtime, strftime
import pytest
from sanic import Sanic, text
from sanic.exceptions import FileNotFound, ServerError

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/test-get")
    async def test_get(request):
        return text('I am get method')

    request, response = app.test_client.get("/test-get")

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")

    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test-get-with-params")
    async def test_get_with_params(request):
        param = request.args.get('param', 'default')
        return text(f'Param is: {param}')

    request, response = app.test_client.get("/test-get-with-params?param=test")

    assert response.status == 200
    assert response.text == 'Param is: test'

def test_get_method_without_query_params(app):
    @app.get("/test-get-with-params")
    async def test_get_with_params(request):
        param = request.args.get('param', 'default')
        return text(f'Param is: {param}')

    request, response = app.test_client.get("/test-get-with-params")

    assert response.status == 200
    assert response.text == 'Param is: default'