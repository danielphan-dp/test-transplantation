import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return mock.create_autospec(web.Application, spec_set=True)

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    ret = mock.Mock()
    ret.set_parser.return_value = ret
    return ret

def test_ipv6_nondefault_https_port_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com', 'UPGRADE': 'websocket'})
    req = make_request("get", "https://[2001:db8::1]:960/", headers=custom_headers)
    assert req.host == "2001:db8::1"
    assert req.port == 960
    assert req.is_ssl()
    assert req.headers['HOST'] == 'custom.example.com'
    assert req.headers['UPGRADE'] == 'websocket'

def test_ipv6_nondefault_https_port_without_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://[2001:db8::1]:960/")
    assert req.host == "2001:db8::1"
    assert req.port == 960
    assert req.is_ssl()
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'

def test_ipv6_nondefault_https_port_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://[2001:db8::1]:960/", protocols=True)
    assert req.host == "2001:db8::1"
    assert req.port == 960
    assert req.is_ssl()
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'