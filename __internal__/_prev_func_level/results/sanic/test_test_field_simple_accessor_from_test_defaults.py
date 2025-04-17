import pytest
from sanic.request import Request
from sanic import Sanic

@pytest.mark.parametrize('headers,expected', (
    ({'foo': 'bar'}, 'bar'),
    ({'foo': 'baz', 'bar': 'qux'}, 'baz'),
    ({'foo': 'bar', 'foo': 'baz'}, 'baz'),
    ({}, ''),
    ({'foo': None}, ''),
    ({'foo': 'bar', 'bar': None}, 'bar'),
))
def test_field_simple_accessor(headers, expected):
    request = make_request(headers)
    assert request.headers.foo == request.headers.foo_ == expected
    assert request.method == 'GET'
    assert request.path_url == b'/'
    assert request.version == '1.1'