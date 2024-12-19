import pytest
from sanic.request import Request
from unittest.mock import Mock

def test_empty_headers():
    request = make_request({})
    assert request.headers == {}

def test_single_header():
    headers = {'Content-Type': 'application/json'}
    request = make_request(headers)
    assert request.headers['Content-Type'] == 'application/json'

def test_multiple_headers():
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer token'}
    request = make_request(headers)
    assert request.headers['Content-Type'] == 'application/json'
    assert request.headers['Authorization'] == 'Bearer token'

def test_invalid_header_access():
    request = make_request({'Content-Type': 'application/json'})
    with pytest.raises(KeyError, match="'Header' object has no attribute '_invalid'"):
        request.headers._invalid

def test_none_headers():
    request = make_request(None)
    assert request.headers == {}