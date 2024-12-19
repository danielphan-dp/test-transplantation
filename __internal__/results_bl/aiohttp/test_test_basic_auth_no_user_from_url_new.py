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

def test_basic_auth_with_user_from_url(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://user:password@python.org")
    assert "AUTHORIZATION" in req.headers
    assert "Basic dXNlcjpwYXNzd29yZA==" == req.headers["AUTHORIZATION"]
    assert "python.org" == req.host

def test_no_auth_from_url(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org")
    assert "AUTHORIZATION" not in req.headers
    assert "python.org" == req.host

def test_auth_with_special_characters_in_user(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://user%20name:pass%20word@python.org")
    assert "AUTHORIZATION" in req.headers
    assert "Basic dXNlciBuYW1lOnBhc3Mgd29yZA==" == req.headers["AUTHORIZATION"]
    assert "python.org" == req.host

def test_auth_with_empty_password(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://user:@python.org")
    assert "AUTHORIZATION" in req.headers
    assert "Basic dXNlcjoi" == req.headers["AUTHORIZATION"]
    assert "python.org" == req.host

def test_auth_with_empty_user(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://:password@python.org")
    assert "AUTHORIZATION" in req.headers
    assert "Basic OnBhc3N3b3Jk" == req.headers["AUTHORIZATION"]
    assert "python.org" == req.host

def test_auth_with_invalid_url_format(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://@python.org")
    assert "AUTHORIZATION" not in req.headers
    assert "python.org" == req.host