import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_params_are_added_with_empty_headers(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path#fragment", headers=CIMultiDict())
    assert str(req.url) == "http://example.com/path#fragment"

def test_params_are_added_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("GET", "http://example.com/path#fragment", headers=headers, params={"a": "b"})
    assert str(req.url) == "http://example.com/path?a=b#fragment"
    assert req.headers['CUSTOM-HEADER'] == 'value'

def test_params_are_added_with_no_fragment(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path", params={"a": "b"})
    assert str(req.url) == "http://example.com/path?a=b"

def test_params_are_added_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_params_are_added_with_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("GET", "invalid-url", params={"a": "b"})