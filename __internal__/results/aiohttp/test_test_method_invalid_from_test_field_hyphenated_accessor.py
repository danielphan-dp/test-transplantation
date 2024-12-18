import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    ret: web.Application = mock.create_autospec(web.Application, spec_set=True)
    return ret

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    ret = mock.Mock()
    return ret

def test_method_invalid_characters(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Method cannot contain non-token characters"):
        make_request("INVALID METHOD!", "http://python.org/")

def test_method_empty(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Method cannot be empty"):
        make_request("", "http://python.org/")

def test_method_valid(make_request: _RequestMaker) -> None:
    request = make_request("GET", "http://python.org/")
    assert request.method == "GET"
    assert request.path == "http://python.org/"

def test_method_with_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'Custom-Header': 'Value'})
    request = make_request("GET", "http://python.org/", headers=headers)
    assert request.headers['Custom-Header'] == 'Value'

def test_method_with_protocols(make_request: _RequestMaker) -> None:
    request = make_request("GET", "http://python.org/", protocols=True)
    assert request.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'