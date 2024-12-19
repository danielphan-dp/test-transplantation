import pytest
from aiohttp import web
from multidict import CIMultiDict
from yarl import URL

@pytest.fixture
def make_request(app: web.Application, protocol: web.RequestHandler[web.Request]) -> _RequestMaker:
    def maker(method: str, path: str, headers: Optional[CIMultiDict[str]]=None, protocols: bool=False) -> web.Request:
        if headers is None:
            headers = CIMultiDict({'HOST': 'server.example.com', 'UPGRADE': 'websocket', 'CONNECTION': 'Upgrade', 'SEC-WEBSOCKET-KEY': 'dGhlIHNhbXBsZSBub25jZQ==', 'ORIGIN': 'http://example.com', 'SEC-WEBSOCKET-VERSION': '13'})
        if protocols:
            headers['SEC-WEBSOCKET-PROTOCOL'] = 'chat, superchat'
        return make_mocked_request(method, path, headers, app=app, protocol=protocol)
    return maker

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
    assert 'SEC-WEBSOCKET-PROTOCOL' in req.headers
    assert req.request_info == aiohttp.RequestInfo(url, "GET", h, url)

def test_request_info_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://python.org/")

def test_request_info_with_empty_path(make_request: _RequestMaker) -> None:
    req = make_request("get", "")
    url = URL("")
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(url, "GET", h, url)

def test_request_info_with_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers=None)
    url = URL("http://python.org/")
    h = CIMultiDictProxy(req.headers)
    assert req.request_info == aiohttp.RequestInfo(url, "GET", h, url)