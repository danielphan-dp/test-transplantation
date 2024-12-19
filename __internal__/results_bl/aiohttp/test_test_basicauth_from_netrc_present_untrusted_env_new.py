import pytest
from aiohttp import hdrs
from multidict import CIMultiDict

@pytest.mark.parametrize('protocols', [True, False])
def test_make_request_with_protocols(make_request, protocols):
    """Test request creation with and without websocket protocols"""
    req = make_request("GET", "http://example.com", protocols=protocols)
    if protocols:
        assert 'SEC-WEBSOCKET-PROTOCOL' in req.headers
    else:
        assert 'SEC-WEBSOCKET-PROTOCOL' not in req.headers

def test_make_request_with_custom_headers(make_request):
    """Test request creation with custom headers"""
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("GET", "http://example.com", headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'

def test_make_request_without_headers(make_request):
    """Test request creation without any headers"""
    req = make_request("GET", "http://example.com", headers=None)
    assert hdrs.AUTHORIZATION not in req.headers
    assert req.headers['HOST'] == 'server.example.com'

def test_make_request_with_invalid_method(make_request):
    """Test request creation with an invalid HTTP method"""
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "http://example.com")