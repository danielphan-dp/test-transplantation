import pytest
from sanic.request import Request
from sanic import Sanic

@pytest.mark.parametrize('headers,expected', (
    ({'foo': 'bar'}, 'bar'),
    ({'foo': 'baz', 'bar': 'qux'}, 'baz'),
    ({'foo': 'bar', 'foo': 'baz'}, 'baz'),
    ({'foo': None}, ''),
    ({}, ''),
))
def test_field_simple_accessor(headers, expected):
    request = make_request(headers)
    assert request.headers.foo == request.headers.foo_ == expected

@pytest.mark.parametrize('headers', (
    {'foo': 'bar', 'bar': 'baz'},
    {'foo': 'bar', 'foo': 'baz', 'baz': 'qux'},
))
def test_field_simple_accessor_multiple_values(headers):
    request = make_request(headers)
    assert request.headers.foo == request.headers.foo_ == headers['foo']

def test_field_simple_accessor_empty_headers():
    request = make_request({})
    assert request.headers.foo == request.headers.foo_ == ''