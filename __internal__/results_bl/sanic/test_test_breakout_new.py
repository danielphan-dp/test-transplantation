import logging
import os
import sys
import collections
from pathlib import Path
from time import gmtime, strftime
import pytest
from sanic import Sanic
from sanic.text import text
from sanic.exceptions import FileNotFound, ServerError

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'