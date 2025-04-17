import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return mock.create_autospec(web.Application, spec_set=True)

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    ret = mock.Mock()
    ret.set_parser.return_value = ret
    return ret

def test_skip_default_useragent_header(make_request: _RequestMaker) -> None:
    req = make_request(
        "get", "http://python.org/", skip_auto_headers={istr("user-agent")}
    )
    assert "User-Agent" not in req.headers

def test_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'X-Custom-Header': 'value'})
    req = make_request("get", "http://python.org/", headers=custom_headers)
    assert req.headers['X-Custom-Header'] == 'value'

def test_with_protocols_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_missing_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers=None)
    assert 'HOST' in req.headers
    assert 'UPGRADE' in req.headers
    assert 'CONNECTION' in req.headers

def test_skip_multiple_auto_headers(make_request: _RequestMaker) -> None:
    req = make_request(
        "get", "http://python.org/", skip_auto_headers={istr("user-agent"), istr("host")}
    )
    assert "User-Agent" not in req.headers
    assert "HOST" not in req.headers

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "http://python.org/")