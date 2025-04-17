import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_query_str_param_is_encoded(make_request: _RequestMaker) -> None:
    for meth in ClientRequest.ALL_METHODS:
        req = make_request(meth, "http://python.org", params="test=f%2Boo")
        assert str(req.url) == "http://python.org/?test=f+oo"

def test_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    for meth in ClientRequest.ALL_METHODS:
        req = make_request(meth, "http://python.org", headers=custom_headers)
        assert req.headers['CUSTOM-HEADER'] == 'value'

def test_request_with_protocols(make_request: _RequestMaker) -> None:
    for meth in ClientRequest.ALL_METHODS:
        req = make_request(meth, "http://python.org", protocols=True)
        assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_request_without_headers(make_request: _RequestMaker) -> None:
    for meth in ClientRequest.ALL_METHODS:
        req = make_request(meth, "http://python.org", headers=None)
        assert req.headers['HOST'] == 'server.example.com'
        assert req.headers['UPGRADE'] == 'websocket'