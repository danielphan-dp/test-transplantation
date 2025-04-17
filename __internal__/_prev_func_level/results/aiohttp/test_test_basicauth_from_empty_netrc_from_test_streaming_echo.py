import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request
from multidict import CIMultiDict
from aiohttp import hdrs

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

@pytest.mark.parametrize("headers, expected_auth", [
    (None, False),
    (CIMultiDict({'Authorization': 'Bearer token'}), True),
    (CIMultiDict({'Authorization': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='}), True),
])
def test_basicauth_with_various_headers(make_request, headers, expected_auth) -> None:
    """Test that Authorization header is sent or not based on input headers"""
    req = make_request("get", "http://example.com", headers=headers)
    assert (hdrs.AUTHORIZATION in req.headers) == expected_auth

def test_basicauth_with_empty_netrc(make_request) -> None:
    """Test that no Authorization header is sent when netrc is empty"""
    req = make_request("get", "http://example.com", trust_env=True)
    assert hdrs.AUTHORIZATION not in req.headers

def test_basicauth_with_invalid_header(make_request) -> None:
    """Test that invalid Authorization header is handled correctly"""
    headers = CIMultiDict({'Authorization': 'InvalidHeader'})
    req = make_request("get", "http://example.com", headers=headers)
    assert hdrs.AUTHORIZATION in req.headers
    assert req.headers[hdrs.AUTHORIZATION] == 'InvalidHeader'