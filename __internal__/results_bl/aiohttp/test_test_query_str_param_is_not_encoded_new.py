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

def test_query_str_param_with_special_characters(make_request: _RequestMaker) -> None:
    for meth in ClientRequest.ALL_METHODS:
        req = make_request(meth, "http://python.org", params="test=f%20oo")
        assert str(req.url) == "http://python.org/?test=f%20oo"

def test_query_str_param_empty(make_request: _RequestMaker) -> None:
    for meth in ClientRequest.ALL_METHODS:
        req = make_request(meth, "http://python.org", params="")
        assert str(req.url) == "http://python.org/?"

def test_query_str_param_multiple_values(make_request: _RequestMaker) -> None:
    for meth in ClientRequest.ALL_METHODS:
        req = make_request(meth, "http://python.org", params={"test": ["value1", "value2"]})
        assert str(req.url) == "http://python.org/?test=value1&test=value2"

def test_query_str_param_with_none_value(make_request: _RequestMaker) -> None:
    for meth in ClientRequest.ALL_METHODS:
        req = make_request(meth, "http://python.org", params={"test": None})
        assert str(req.url) == "http://python.org/?test=None"