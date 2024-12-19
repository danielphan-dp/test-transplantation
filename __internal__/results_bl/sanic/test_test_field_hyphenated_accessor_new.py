import pytest
from sanic.request import Request
from sanic import make_request

@pytest.mark.parametrize('headers,expected', [
    ({'foo-bar': 'bar'}, 'bar'),
    ({'foo-bar': 'baz'}, 'baz'),
    ({'foo-bar': None}, None),
    ({'foo-bar': ''}, ''),
    ({'foo-bar': 'value1', 'foo-bar': 'value2'}, 'value2'),
    ({'foo-bar': 'value1', 'foo-bar_': 'value2'}, 'value2'),
    ({'foo-bar': 'value1', 'foo-bar_': None}, None),
    ({'foo-bar': 'value1', 'foo-bar_': ''}, ''),
])
def test_make_request_with_hyphenated_headers(headers, expected):
    request = make_request(headers)
    assert request.headers.foo_bar == request.headers.foo_bar_ == expected

@pytest.mark.parametrize('headers', [
    ({'foo-bar': 'bar', 'foo-bar_': 'bar'}),
    ({'foo-bar': 'bar', 'foo-bar_': 'baz'}),
    ({'foo-bar': 'bar', 'foo-bar_': None}),
])
def test_make_request_with_duplicate_hyphenated_headers(headers):
    request = make_request(headers)
    assert request.headers.foo_bar == request.headers.foo_bar_