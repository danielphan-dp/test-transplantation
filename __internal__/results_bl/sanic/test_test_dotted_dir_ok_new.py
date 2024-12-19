import logging
import os
import sys
import collections
from pathlib import Path
import time
from time import gmtime, strftime
import pytest
from sanic import Sanic
from sanic.text import text
from sanic.exceptions import FileNotFound, ServerError

@pytest.mark.skipif(sys.platform == 'win32', reason='Windows does not support double dotted directories')
def test_get_method(app: Sanic):
    request = {}
    response = app.get(request)
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_with_invalid_request(app: Sanic):
    request = None
    with pytest.raises(TypeError):
        app.get(request)

def test_get_method_with_empty_request(app: Sanic):
    request = {}
    response = app.get(request)
    assert response.status == 200
    assert response.body == b'I am get method'