import pytest
from aiohttp import web
from multidict import CIMultiDict
from yarl import URL

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_request_info_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "http://python.org/", headers=custom_headers)
    url = URL("http://python.org/")
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(url, "GET", h, url)

def test_request_info_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    url = URL("http://python.org/")
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(url, "GET", h, url)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_request_info_with_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers=None)
    url = URL("http://python.org/")
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(url, "GET", h, url)

def test_request_info_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://python.org/")