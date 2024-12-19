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

def test_missing_auth_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org")
    assert "AUTHORIZATION" not in req.headers

def test_invalid_auth_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org", auth=aiohttp.BasicAuth("invalid_user", "wrong_password"))
    assert "AUTHORIZATION" in req.headers
    assert req.headers["AUTHORIZATION"] != "Basic aW52YWxpZF91c2VyOndyb25nX3Bhc3N3b3Jk"

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'custom_value'})
    req = make_request("get", "http://python.org", headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'custom_value'

def test_websocket_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org", protocols=True)
    assert "SEC-WEBSOCKET-PROTOCOL" in req.headers
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == 'chat, superchat'