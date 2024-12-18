import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_gen_netloc_with_port(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "https://aiohttp:pwpwpw@123.45.67.89:8080/"
    )
    assert req.headers["HOST"] == "123.45.67.89:8080"

def test_gen_netloc_empty_path(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "https://aiohttp:pwpwpw@123.45.67.89/"
    )
    assert req.headers["HOST"] == "123.45.67.89"

def test_gen_netloc_with_subdomain(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "https://aiohttp:pwpwpw@subdomain.example.com/"
    )
    assert req.headers["HOST"] == "subdomain.example.com"

def test_gen_netloc_with_special_characters(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "https://aiohttp:pwpwpw@123.45.67.89:8080/path?query=param#fragment"
    )
    assert req.headers["HOST"] == "123.45.67.89:8080"

def test_gen_netloc_no_scheme(make_request: _RequestMaker) -> None:
    req = make_request(
        "get",
        "aiohttp:pwpwpw@123.45.67.89/"
    )
    assert req.headers["HOST"] == "123.45.67.89"