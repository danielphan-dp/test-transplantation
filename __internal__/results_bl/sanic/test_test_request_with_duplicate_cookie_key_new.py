import pytest
from sanic import Sanic
from sanic.response import text
from unittest.mock import Mock
from sanic.compat import Header
from sanic.request import Request

app = Sanic("TestApp")

@app.get("/")
def get(request):
    return text('I am get method')

@pytest.mark.parametrize('value', ('foo=one; foo=two', 'foo=one;foo=two', 'foo=three; foo=four', 'foo=; foo=two', 'foo=one; bar=two'))
def test_request_with_duplicate_cookie_key(value):
    headers = Header({"Cookie": value})
    request = Request(b"/", headers, "1.1", "GET", Mock(), Mock())

    assert request.cookies["foo"] in ["one", "three", ""]
    assert request.cookies.get("foo") in ["one", "three", None]
    assert request.cookies.getlist("foo") in [["one", "two"], ["three", "four"], ["", "two"]]
    assert request.cookies.get("bar") in [None, "two"]