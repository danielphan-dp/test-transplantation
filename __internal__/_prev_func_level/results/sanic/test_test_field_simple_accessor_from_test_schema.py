import pytest
from sanic.request import Request
from sanic import Sanic

@pytest.mark.parametrize('headers,expected', [
    ({'foo': 'bar'}, 'bar'),
    ({'foo': 'baz'}, 'baz'),
    ({'foo': 'bar', 'baz': 'qux'}, 'bar'),
    ({'foo': 'bar', 'foo': 'baz'}, 'baz'),
    ({}, ''),
    ({'foo': None}, ''),
    ({'foo': 'bar', 'foo2': 'baz'}, 'bar'),
])
def test_field_simple_accessor(headers, expected):
    request = make_request(headers)
    assert request.headers.foo == request.headers.foo_ == expected

@pytest.mark.parametrize('headers', [
    ({'foo': 'bar'}),
    ({'foo': 'baz'}),
    ({'foo': 'bar', 'baz': 'qux'}),
    ({'foo': None}),
])
def test_field_simple_accessor_with_none(headers):
    request = make_request(headers)
    assert request.headers.foo is not None

def test_field_simple_accessor_empty():
    request = make_request({})
    assert request.headers.foo == request.headers.foo_ == ''