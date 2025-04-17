import pytest
from multidict import CIMultiDict
from aiohttp import web

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return mock.create_autospec(web.Application, spec_set=True)

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    ret = mock.Mock()
    ret.set_parser.return_value = ret
    return ret

def test_cookies_merge_with_multiple_headers(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        headers={"cookie": "cookie1=val1", "another-header": "value"},
        cookies={"cookie2": "val2"},
    )
    assert "cookie1=val1; cookie2=val2" == req.headers["COOKIE"]

def test_cookies_with_no_headers(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        cookies={"cookie2": "val2"},
    )
    assert "cookie2=val2" == req.headers["COOKIE"]

def test_cookies_with_empty_headers(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        headers={},
        cookies={"cookie2": "val2"},
    )
    assert "cookie2=val2" == req.headers["COOKIE"]

def test_cookies_with_empty_cookies(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        headers={"cookie": "cookie1=val1"},
        cookies={},
    )
    assert "cookie1=val1" == req.headers["COOKIE"]

def test_cookies_merge_with_special_characters(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        headers={"cookie": "cookie1=val1; cookie3=val3;"},
        cookies={"cookie2": "val2"},
    )
    assert "cookie1=val1; cookie2=val2; cookie3=val3" == req.headers["COOKIE"]