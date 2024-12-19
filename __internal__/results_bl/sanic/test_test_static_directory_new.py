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

@pytest.mark.parametrize('base_uri', ['/static', '', '/dir'])
@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'symlink', 'hard_link'])
def test_get_method(app, base_uri, file_name):
    request, response = app.test_client.get(uri=f"{base_uri}/{file_name}")
    assert response.status == 200
    assert response.body == text('I am get method')

def test_get_method_not_found(app):
    request, response = app.test_client.get(uri='/nonexistent')
    assert response.status == 404

def test_get_method_empty_uri(app):
    request, response = app.test_client.get(uri='')
    assert response.status == 200
    assert response.body == text('I am get method')