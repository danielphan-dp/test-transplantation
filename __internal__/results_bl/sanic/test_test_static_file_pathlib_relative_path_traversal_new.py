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

@pytest.mark.parametrize('request_path', ['/valid_path', '/another_valid_path', '/invalid_path'])
def test_get_method(app, request_path):
    """Test the get method of the app with various request paths."""
    response = app.test_client.get(request_path)
    
    if request_path in ['/valid_path', '/another_valid_path']:
        assert response.status == 200
        assert response.body == b'I am get method'
    else:
        assert response.status == 404  # Assuming invalid paths return 404