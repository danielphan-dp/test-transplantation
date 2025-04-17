import pytest
from sanic.request import Request
from sanic import Sanic

def make_request(headers) -> Request:
    return Request(b'/', headers, '1.1', 'GET', None, None)

def test_make_request_empty_headers():
    request = make_request({})
    assert request.headers == {}

def test_make_request_with_single_header():
    request = make_request({'X-Test-Header': 'value'})
    assert request.headers['X-Test-Header'] == 'value'

def test_make_request_with_multiple_headers():
    headers = {
        'X-Foo': 'bar',
        'X-Baz': 'qux'
    }
    request = make_request(headers)
    assert request.headers['X-Foo'] == 'bar'
    assert request.headers['X-Baz'] == 'qux'

def test