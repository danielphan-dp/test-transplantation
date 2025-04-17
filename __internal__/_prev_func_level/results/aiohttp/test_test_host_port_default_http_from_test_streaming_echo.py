import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_host_port_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com', 'USER-AGENT': 'test-agent'})
    req = make_request("get", "http://custom.example.com/", headers=custom_headers)
    assert req.host == "custom.example.com"
    assert req.port == 80
    assert not req.is_ssl()
    assert req.headers['USER-AGENT'] == 'test-agent'

def test_host_port_https(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://secure.example.com/")
    assert req.host == "secure.example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_port_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "invalid-url")

def test_host_port_with_query_params(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/?query=param")
    assert req.host == "python.org"
    assert req.port == 80
    assert not req.is_ssl()
    assert req.query['query'] == 'param'