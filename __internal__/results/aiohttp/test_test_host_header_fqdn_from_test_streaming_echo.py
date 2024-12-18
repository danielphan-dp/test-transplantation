import pytest
from multidict import CIMultiDict
from aiohttp import web

@pytest.mark.parametrize(('url', 'headers', 'expected'), [
    pytest.param('http://localhost.', None, 'localhost', id='dot only at the end'),
    pytest.param('http://python.org.', None, 'python.org', id='single dot'),
    pytest.param('http://python.org.:99', None, 'python.org:99', id='single dot with port'),
    pytest.param('http://python.org...:99', None, 'python.org:99', id='multiple dots with port'),
    pytest.param('http://python.org.:99', {'host': 'example.com.:99'}, 'example.com.:99', id='explicit host header'),
    pytest.param('https://python.org.', None, 'python.org', id='https'),
    pytest.param('https://...', None, '', id='only dots'),
    pytest.param('http://príklad.example.org.:99', None, 'xn--prklad-4va.example.org:99', id='single dot with port idna'),
    pytest.param('http://example.com', {'HOST': 'custom.host'}, 'custom.host', id='custom host header'),
    pytest.param('http://example.com', {'HOST': 'example.com:80'}, 'example.com:80', id='host with default port'),
])
def test_host_header_fqdn(make_request, url, headers, expected):
    req = make_request("get", url, headers=headers)
    assert req.headers["HOST"] == expected

def test_host_header_with_protocols(make_request):
    headers = CIMultiDict({'HOST': 'server.example.com', 'SEC-WEBSOCKET-PROTOCOL': 'chat'})
    req = make_request("get", '/path', headers=headers, protocols=True)
    assert req.headers["HOST"] == 'server.example.com'
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == 'chat'

def test_host_header_empty(make_request):
    req = make_request("get", '/path', headers=CIMultiDict())
    assert req.headers["HOST"] == 'server.example.com'  # Default header value

def test_host_header_invalid_url(make_request):
    with pytest.raises(ValueError):
        make_request("get", 'invalid-url', headers=None)