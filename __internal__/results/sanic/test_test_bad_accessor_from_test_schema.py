import pytest
from sanic.request import Request
from sanic import Sanic

def make_request(headers) -> Request:
    return Request(b'/', headers, '1.1', 'GET', None, None)

def test_empty_headers():
    request = make_request({})
    assert request.headers == {}

def test_single_header():
    request = make_request({'X-Custom-Header': 'value'})
    assert request.headers['X-Custom-Header'] == 'value'

def test_multiple_headers():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer token',
        'X-Custom-Header': 'value'
    }
    request = make_request(headers)
    assert request.headers['Content-Type'] == 'application/json'
    assert request.headers['Authorization'] == 'Bearer token'
    assert request.headers['X-Custom-Header'] == 'value'

def test_invalid_header_access():
    request = make_request({'X-Custom-Header': 'value'})
    with pytest.raises(AttributeError, match="'Header' object has no attribute '_foo'"):
        request.headers._foo

def test_header_case_insensitivity():
    headers = {
        'content-type': 'application/json',
        'AUTHORIZATION': 'Bearer token'
    }
    request = make_request(headers)
    assert request.headers['Content-Type'] == 'application/json'
    assert request.headers['Authorization'] == 'Bearer token'

def test_header_with_special_characters():
    headers = {
        'X-Header-With-Special-Characters': 'value@123'
    }
    request = make_request(headers)
    assert request.headers['X-Header-With-Special-Characters'] == 'value@123'