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

def test_include_useragent_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    assert "User-Agent" in req.headers

def test_custom_useragent_header(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'User-Agent': 'CustomAgent/1.0'})
    req = make_request("get", "http://python.org/", headers=custom_headers)
    assert req.headers['User-Agent'] == 'CustomAgent/1.0'

def test_skip_multiple_auto_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", skip_auto_headers={istr("user-agent"), istr("host")})
    assert "User-Agent" not in req.headers
    assert "Host" not in req.headers

def test_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers=CIMultiDict())
    assert "User-Agent" in req.headers
    assert req.headers['User-Agent'] == 'aiohttp/3.8.1'  # Assuming default User-Agent

def test_protocols_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    assert 'SEC-WEBSOCKET-PROTOCOL' in req.headers
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'