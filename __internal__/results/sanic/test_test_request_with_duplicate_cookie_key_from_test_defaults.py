import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

app = Sanic("test_app")

class DummyView:
    def get(self, request):
        return text('I am get method')

@app.get("/")
async def handler(request: Request):
    return DummyView().get(request)

@pytest.mark.parametrize('value', ('foo=one; foo=two', 'foo=one;foo=two'))
def test_get_method_with_duplicate_cookie_key(value):
    headers = {"Cookie": value}
    request = Request(b"/", headers, "1.1", "GET", None, None)

    response = handler(request)
    
    assert response.status == 200
    assert response.body == b'I am get method'
    assert request.cookies["foo"] == "one"
    assert request.cookies.get("foo") == "one"
    assert request.cookies.getlist("foo") == ["one", "two"]
    assert request.cookies.get("bar") is None

def test_get_method_without_cookies():
    headers = {}
    request = Request(b"/", headers, "1.1", "GET", None, None)

    response = handler(request)
    
    assert response.status == 200
    assert response.body == b'I am get method'
    assert request.cookies.get("foo") is None
    assert request.cookies.get("bar") is None

def test_get_method_with_invalid_cookie_format():
    headers = {"Cookie": "invalid_format"}
    request = Request(b"/", headers, "1.1", "GET", None, None)

    response = handler(request)
    
    assert response.status == 200
    assert response.body == b'I am get method'
    assert request.cookies.get("foo") is None
    assert request.cookies.get("bar") is None