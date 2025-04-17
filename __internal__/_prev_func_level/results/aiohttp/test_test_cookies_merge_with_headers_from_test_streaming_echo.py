import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_cookies_merge_with_headers_and_empty_headers(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        headers={},
        cookies={"cookie1": "val1", "cookie2": "val2"},
    )
    assert "cookie1=val1; cookie2=val2" == req.headers["COOKIE"]

def test_cookies_merge_with_headers_and_no_cookies(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        headers={"cookie": "cookie1=val1"},
        cookies={},
    )
    assert "cookie1=val1" == req.headers["COOKIE"]

def test_cookies_merge_with_headers_and_multiple_cookies(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        headers={"cookie": "cookie1=val1"},
        cookies={"cookie2": "val2", "cookie3": "val3"},
    )
    assert "cookie1=val1; cookie2=val2; cookie3=val3" == req.headers["COOKIE"]

def test_cookies_merge_with_headers_and_special_characters(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        headers={"cookie": "cookie1=val1; cookie2=val2"},
        cookies={"cookie3": "val3; path=/"},
    )
    assert "cookie1=val1; cookie2=val2; cookie3=val3; path=/" == req.headers["COOKIE"]

def test_cookies_merge_with_headers_and_empty_cookies(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "http://test.com/path",
        headers={"cookie": "cookie1=val1"},
        cookies={},
    )
    assert "cookie1=val1" == req.headers["COOKIE"]