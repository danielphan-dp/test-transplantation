import logging
import os
import sys
import collections
from pathlib import Path
from time import gmtime, strftime
import pytest
from sanic import Sanic, text
from sanic.exceptions import FileNotFound, ServerError

@pytest.mark.skipif(sys.platform != 'win32', reason='Block backslash on Windows only')
def test_get_method(app: Sanic):
    request = app.test_client.get('/get')
    assert request.status == 200
    assert request.text == 'I am get method'

def test_get_method_invalid_route(app: Sanic):
    request = app.test_client.get('/invalid')
    assert request.status == 404

def test_get_method_with_query_params(app: Sanic):
    request = app.test_client.get('/get?param=value')
    assert request.status == 200
    assert request.text == 'I am get method'