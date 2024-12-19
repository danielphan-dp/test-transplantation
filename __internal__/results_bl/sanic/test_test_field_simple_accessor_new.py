import pytest
from sanic.request import Request
from unittest.mock import Mock

@pytest.mark.parametrize('headers,expected', [
    ({'foo': 'bar'}, 'bar'),
    ({'foo': 'baz'}, 'baz'),
    ({'foo': None}, ''),
    ({}, ''),
    ({'foo': 'bar', 'baz': 'qux'}, 'bar'),
    ({('foo', 'bar'), ('foo', 'baz')}, 'bar,baz'),
    ({'foo': 'bar', 'foo': 'baz'}, 'baz'),
])
def test_field_simple_accessor(headers, expected):
    request = make_request(headers)
    assert request.headers.foo == request.headers.foo_ == expected

def test_field_simple_accessor_empty_headers():
    request = make_request({})
    assert request.headers.foo == request.headers.foo_ == ''

def test_field_simple_accessor_invalid_header():
    with pytest.raises(Exception):
        make_request({'invalid-header': 'value'})