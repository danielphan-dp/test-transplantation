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
    view = DummyView()
    return view.get(request)

@pytest.mark.parametrize('value', [
    ('foo=one; foo=two'),
    ('foo=one;foo=two'),
    ('foo=three; foo=four; foo=five'),
    ('foo=one; bar=two; foo=three'),
    ('foo=; foo=two'),
    ('foo=one; bar=; foo=three')
])
def test_get_method_with_duplicate_cookie_key(value):
    headers = {"Cookie": value}
    request = Request(b"/", headers, "1.1", "GET", Mock(), Mock())
    
    response = handler(request)
    
    assert response.text == 'I am get method'
    assert request.cookies.get("foo") in ["one", "two", "three"]
    assert request.cookies.get("bar") is None
    assert request.cookies.getlist("foo") == ["one", "two", "three"] or request.cookies.getlist("foo") == ["one", "two"] or request.cookies.getlist("foo") == ["three"]