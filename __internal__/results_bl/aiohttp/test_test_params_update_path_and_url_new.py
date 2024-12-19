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

def test_params_update_path_with_empty_params(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org", params=())
    assert str(req.url) == "http://python.org/"

def test_params_update_path_with_single_param(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org", params=(("test", "foo"),))
    assert str(req.url) == "http://python.org/?test=foo"

def test_params_update_path_with_special_characters(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org", params=(("test", "foo bar"),))
    assert str(req.url) == "http://python.org/?test=foo+bar"

def test_params_update_path_with_duplicate_keys(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org", params=(("test", "foo"), ("test", "baz")))
    assert str(req.url) == "http://python.org/?test=foo&test=baz"

def test_params_update_path_with_none_params(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org", params=None)
    assert str(req.url) == "http://python.org/"

def test_params_update_path_with_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "invalid_url", params=(("test", "foo"),))