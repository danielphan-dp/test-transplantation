import pytest
from multidict import CIMultiDict
from aiohttp import web

@pytest.mark.parametrize(('url', 'headers', 'expected'), 
    [
        pytest.param('http://localhost.', None, 'localhost', id='dot only at the end'),
        pytest.param('http://python.org.', None, 'python.org', id='single dot'),
        pytest.param('http://python.org.:99', None, 'python.org:99', id='single dot with port'),
        pytest.param('http://python.org...:99', None, 'python.org:99', id='multiple dots with port'),
        pytest.param('http://python.org.:99', {'host': 'example.com.:99'}, 'example.com.:99', id='explicit host header'),
        pytest.param('https://python.org.', None, 'python.org', id='https'),
        pytest.param('https://...', None, '', id='only dots'),
        pytest.param('http://príklad.example.org.:99', None, 'xn--prklad-4va.example.org:99', id='single dot with port idna'),
        pytest.param('http://example.com', {'HOST': 'custom.host'}, 'custom.host', id='custom host header'),
        pytest.param('http://example.com', {'HOST': 'example.com'}, 'example.com', id='default host header'),
        pytest.param('http://example.com', {'HOST': 'invalid..host'}, 'invalid..host', id='invalid host with double dot'),
        pytest.param('http://example.com', {'HOST': '123.456.789.000'}, '123.456.789.000', id='numeric host'),
    ]
)
def test_host_header_edge_cases(make_request, url, headers, expected):
    req = make_request("get", url, headers=headers)
    assert req.headers["HOST"] == expected