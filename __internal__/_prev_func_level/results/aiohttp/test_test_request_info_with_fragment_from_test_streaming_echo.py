import pytest
from aiohttp import web
from multidict import CIMultiDict, CIMultiDictProxy
from yarl import URL

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_request_info_with_no_fragment(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(
        URL("http://python.org/"),
        "GET",
        h,
        URL("http://python.org/")
    )

def test_request_info_with_invalid_url(make_request: _RequestMaker) -> None:
    req = make_request("get", "invalid_url")
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(
        URL("invalid_url"),
        "GET",
        h,
        URL("invalid_url")
    )

def test_request_info_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'X-Custom-Header': 'value'})
    req = make_request("get", "http://python.org/", headers=custom_headers)
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(
        URL("http://python.org/"),
        "GET",
        h,
        URL("http://python.org/")
    )
    assert req.headers['X-Custom-Header'] == 'value'

def test_request_info_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(
        URL("http://python.org/"),
        "GET",
        h,
        URL("http://python.org/")
    )
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'