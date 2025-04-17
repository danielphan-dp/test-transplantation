import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_ipv6_custom_http_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://[2001:db8::1]:8080/")
    assert req.host == "2001:db8::1"
    assert req.port == 8080
    assert not req.is_ssl()

def test_ipv6_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "http://[2001:db8::1]/", headers=headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'
    assert req.host == "2001:db8::1"
    assert req.port == 80
    assert not req.is_ssl()

def test_ipv6_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://[2001:db8::1]/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'
    assert req.host == "2001:db8::1"
    assert req.port == 80
    assert not req.is_ssl()

def test_ipv6_invalid_request(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "http://[invalid::address]/")