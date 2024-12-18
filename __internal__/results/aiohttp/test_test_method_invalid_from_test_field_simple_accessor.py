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

def test_method_invalid_method_with_special_characters(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Method cannot contain non-token characters"):
        make_request("GET@", "http://python.org/")

def test_method_invalid_empty_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Method cannot be empty"):
        make_request("", "http://python.org/")

def test_method_invalid_method_with_control_characters(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Method cannot contain non-token characters"):
        make_request("GET\n", "http://python.org/")

def test_method_invalid_path_with_spaces(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Path cannot contain spaces"):
        make_request("GET", "http://python.org/some path")

def test_method_invalid_headers(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Invalid header name"):
        make_request("GET", "http://python.org/", headers=CIMultiDict({b'Invalid-Header': 'value'}))