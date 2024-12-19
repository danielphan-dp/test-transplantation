import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def make_request(app: web.Application, protocol: web.RequestHandler[web.Request]) -> _RequestMaker:
    def maker(method: str, path: str, headers: Optional[CIMultiDict[str]]=None, protocols: bool=False) -> web.Request:
        if headers is None:
            headers = CIMultiDict({'HOST': 'server.example.com', 'UPGRADE': 'websocket', 'CONNECTION': 'Upgrade', 'SEC-WEBSOCKET-KEY': 'dGhlIHNhbXBsZSBub25jZQ==', 'ORIGIN': 'http://example.com', 'SEC-WEBSOCKET-VERSION': '13'})
        if protocols:
            headers['SEC-WEBSOCKET-PROTOCOL'] = 'chat, superchat'
        return make_mocked_request(method, path, headers, app=app, protocol=protocol)
    return maker

def test_host_header_with_custom_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org:8080/")
    assert req.headers["HOST"] == "python.org:8080"

def test_host_header_with_no_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    assert req.headers["HOST"] == "python.org"

def test_host_header_with_ip_address(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://192.168.1.1/")
    assert req.headers["HOST"] == "192.168.1.1"

def test_host_header_with_empty_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers=CIMultiDict())
    assert req.headers["HOST"] == "server.example.com"

def test_host_header_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"