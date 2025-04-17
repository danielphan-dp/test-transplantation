import pytest
from sanic.request import Request
from sanic import Sanic

@pytest.mark.parametrize('headers,expected', (
    ({'foo-bar': 'bar'}, 'bar'),
    ({'foo-bar': 'baz'}, 'baz'),
    ({'foo-bar': 'bar,baz'}, 'bar,baz'),
    ({'foo-bar': None}, None),
    ({'foo-bar': ''}, ''),
    ({'foo-bar': 'value1,value2'}, 'value1,value2'),
))
def test_field_hyphenated_accessor(headers, expected):
    request = make_request(headers)
    assert request.headers.foo_bar == request.headers.foo_bar_ == expected

@pytest.mark.parametrize('headers', (
    {'foo-bar': 'bar'},
    {'foo-bar': 'baz'},
    {'foo-bar': 'bar,baz'},
))
def test_field_hyphenated_accessor_with_different_cases(headers):
    request = make_request(headers)
    assert request.headers.foo_bar.lower() == request.headers.foo_bar_.lower()

def test_field_hyphenated_accessor_empty_header():
    headers = {}
    request = make_request(headers)
    assert request.headers.foo_bar is None
    assert request.headers.foo_bar_ is None

def test_field_hyphenated_accessor_invalid_header():
    headers = {'foo-bar': 'invalid_value'}
    request = make_request(headers)
    assert request.headers.foo_bar == 'invalid_value'
    assert request.headers.foo_bar_ == 'invalid_value'