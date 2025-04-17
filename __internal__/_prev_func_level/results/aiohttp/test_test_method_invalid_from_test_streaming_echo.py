import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_method_invalid_method_with_special_characters(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Method cannot contain non-token characters"):
        make_request("GET /path", "http://python.org/")

def test_method_invalid_empty_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Method cannot be empty"):
        make_request("", "http://python.org/")

def test_method_invalid_invalid_path(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Path cannot be empty"):
        make_request("GET", "")

def test_method_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    request = make_request("GET", "/path", headers=headers)
    assert request.headers['CUSTOM-HEADER'] == 'value'

def test_method_with_protocols(make_request: _RequestMaker) -> None:
    request = make_request("GET", "/path", protocols=True)
    assert request.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'