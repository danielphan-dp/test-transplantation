import pytest
from multidict import CIMultiDict, CIMultiDictProxy
from yarl import URL
from aiohttp import web

@pytest.fixture
def make_request(app: web.Application, protocol: web.RequestHandler[web.Request]) -> _RequestMaker:
    def maker(method: str, path: str, headers: Optional[CIMultiDict[str]]=None, protocols: bool=False) -> web.Request:
        if headers is None:
            headers = CIMultiDict({'HOST': 'server.example.com', 'UPGRADE': 'websocket', 'CONNECTION': 'Upgrade', 'SEC-WEBSOCKET-KEY': 'dGhlIHNhbXBsZSBub25jZQ==', 'ORIGIN': 'http://example.com', 'SEC-WEBSOCKET-VERSION': '13'})
        if protocols:
            headers['SEC-WEBSOCKET-PROTOCOL'] = 'chat, superchat'
        return make_mocked_request(method, path, headers, app=app, protocol=protocol)
    return maker

def test_request_info_with_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(
        URL("http://python.org/"),
        "GET",
        h,
        URL("http://python.org/")
    )

def test_request_info_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "http://python.org/", headers=custom_headers)
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(
        URL("http://python.org/"),
        "GET",
        h,
        URL("http://python.org/")
    )

def test_request_info_with_invalid_url(make_request: _RequestMaker) -> None:
    req = make_request("get", "invalid-url")
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(
        URL("invalid-url"),
        "GET",
        h,
        URL("invalid-url")
    )

def test_request_info_with_websocket_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(
        URL("http://python.org/"),
        "GET",
        h,
        URL("http://python.org/")
    )