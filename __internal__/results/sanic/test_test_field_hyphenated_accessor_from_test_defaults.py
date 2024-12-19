import pytest
from sanic.request import Request
from sanic import Sanic

@pytest.mark.parametrize('headers,expected', (
    ({'foo-bar': 'bar'}, 'bar'),
    ({'foo-bar': 'baz'}, 'baz'),
    ({'foo-bar': 'bar,baz'}, 'bar,baz'),
    ({'foo-bar': None}, None),
    ({'foo-bar': ''}, ''),
))
def test_make_request_headers(headers, expected):
    request = make_request(headers)
    assert request.headers.foo_bar == expected
    assert request.headers.foo_bar_ == expected
    assert request.headers.get('foo-bar') == expected
    assert request.headers.get('foo-bar_') == expected

def test_make_request_default_values():
    headers = {}
    request = make_request(headers)
    assert request.method == 'GET'
    assert request.path == '/'
    assert request.version == '1.1'
    assert request.headers == headers
    assert request.content_length is None
    assert request.environ.get('PATH_INFO') is None
    assert request.cookies == {}
    assert request.params == {}
    assert request.path_info == '/'
    assert request.script_name == ''
    assert request.path_qs == ''
    assert request.view_name == ''
    assert request.subpath == ()
    assert request.context is None
    assert request.root is None
    assert request.virtual_root is None
    assert request.virtual_root_path == ()