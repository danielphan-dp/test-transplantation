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

def test_host_header_default(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    assert req.headers["HOST"] == "server.example.com"

def test_host_header_no_host(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers={})
    assert req.headers["HOST"] == "server.example.com"

def test_host_header_empty_string(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers={"host": ""})
    assert req.headers["HOST"] == ""

def test_host_header_invalid_format(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers={"host": "invalid_host_format"})
    assert req.headers["HOST"] == "invalid_host_format"

def test_host_header_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers={"host": "example.com"}, protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"