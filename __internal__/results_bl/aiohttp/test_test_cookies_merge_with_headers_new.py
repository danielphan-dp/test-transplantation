import pytest
from multidict import CIMultiDict
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

def test_empty_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://test.com/path", headers={})
    assert req.headers["COOKIE"] == ""

def test_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://test.com/path")
    assert "COOKIE" not in req.headers

def test_multiple_cookies(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        headers={"cookie": "cookie1=val1; cookie2=val2"},
        cookies={"cookie3": "val3"},
    )
    assert "cookie1=val1; cookie2=val2; cookie3=val3" == req.headers["COOKIE"]

def test_protocols_header(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        protocols=True
    )
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://test.com/path")