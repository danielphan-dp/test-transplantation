import unittest
from unittest.mock import Mock
import pytest
from sanic import Sanic
from sanic import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/get")
    async def get_handler(request: Request):
        return text('I am get method')
    return app

def test_get_method_response(app):
    _, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_headers(app):
    _, response = app.test_client.get("/get", headers={"Example-Field": "Test"})
    assert response.text == 'I am get method'

def test_get_method_empty_response(app):
    _, response = app.test_client.get("/get", headers={})
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    _, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    _, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'