import asyncio
import logging
import re
from collections import Counter
import inspect
import os
from unittest.mock import Mock, patch
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.router import Route

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_app_get_method_returns_text(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    _, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_app_get_method_with_invalid_route(app):
    _, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_app_get_method_with_empty_request(app):
    @app.get("/empty")
    def handler(request):
        return text("I am get method with empty request")

    _, response = app.test_client.get("/empty", data={})
    assert response.text == "I am get method with empty request"