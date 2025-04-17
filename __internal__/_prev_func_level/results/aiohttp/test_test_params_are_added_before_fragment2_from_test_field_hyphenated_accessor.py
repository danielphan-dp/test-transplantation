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

def test_params_are_added_with_empty_headers(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path", headers=CIMultiDict())
    assert str(req.url) == "http://example.com/path?HOST=server.example.com&UPGRADE=websocket&CONNECTION=Upgrade&SEC-WEBSOCKET-KEY=dGhlIHNhbXBsZSBub25jZQ==&ORIGIN=http://example.com&SEC-WEBSOCKET-VERSION=13"

def test_params_are_added_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("GET", "http://example.com/path", headers=headers)
    assert str(req.url) == "http://example.com/path?CUSTOM-HEADER=value"

def test_params_are_added_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path", protocols=True)
    assert 'SEC-WEBSOCKET-PROTOCOL' in req.headers
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_params_are_added_with_query_string(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path?key=value", params={"a": "b"})
    assert str(req.url) == "http://example.com/path?key=value&a=b"

def test_params_are_added_with_fragment(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path?key=value#fragment", params={"a": "b"})
    assert str(req.url) == "http://example.com/path?key=value&a=b"