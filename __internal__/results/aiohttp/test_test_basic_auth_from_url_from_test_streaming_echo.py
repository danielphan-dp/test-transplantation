import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_basic_auth_with_invalid_url(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://invalid:wrong@python.org")
    assert "AUTHORIZATION" in req.headers
    assert "Basic aW52YWxpZDp3cm9uZw==" == req.headers["AUTHORIZATION"]
    assert "python.org" == req.host

def test_basic_auth_without_credentials(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org")
    assert "AUTHORIZATION" not in req.headers
    assert "python.org" == req.host

def test_basic_auth_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "http://nkim:1234@python.org", headers=custom_headers)
    assert "AUTHORIZATION" in req.headers
    assert "Basic bmtpbToxMjM0" == req.headers["AUTHORIZATION"]
    assert "value" == req.headers["CUSTOM-HEADER"]
    assert "python.org" == req.host

def test_basic_auth_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://nkim:1234@python.org", protocols=True)
    assert "AUTHORIZATION" in req.headers
    assert "Basic bmtpbToxMjM0" == req.headers["AUTHORIZATION"]
    assert "chat, superchat" == req.headers["SEC-WEBSOCKET-PROTOCOL"]
    assert "python.org" == req.host

def test_basic_auth_with_empty_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://nkim:1234@python.org", headers=CIMultiDict())
    assert "AUTHORIZATION" in req.headers
    assert "Basic bmtpbToxMjM0" == req.headers["AUTHORIZATION"]
    assert "python.org" == req.host