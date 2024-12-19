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

def test_gen_netloc_with_port(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "https://aiohttp:pwpwpw@"
        + "123.456.789.012:8080/"
    )
    assert req.headers["HOST"] == "123.456.789.012:8080"

def test_gen_netloc_empty_path(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "https://aiohttp:pwpwpw@"
        + "example.com/"
    )
    assert req.headers["HOST"] == "example.com"

def test_gen_netloc_no_scheme(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "aiohttp:pwpwpw@"
        + "example.com/"
    )
    assert req.headers["HOST"] == "example.com"

def test_gen_netloc_special_characters(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "https://aiohttp:pwpwpw@"
        + "ex@mple.com/"
    )
    assert req.headers["HOST"] == "ex@mple.com"

def test_gen_netloc_long_hostname(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "https://aiohttp:pwpwpw@"
        + "a" * 64 + ".com/"
    )
    assert req.headers["HOST"] == "a" * 64 + ".com"