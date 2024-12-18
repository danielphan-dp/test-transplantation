import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('max_age', ['0', 30, '30', -1, 'invalid'])
def test_get_method_with_cookies(app, max_age):
    cookies = {"test": "wait"}

    @app.get("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get(
        "/", cookies=cookies, raw_cookies=True
    )
    assert response.status == 200
    assert response.text == "I am get method"

    cookie = response.cookies.get("test")
    if str(max_age).isdigit() and int(max_age) != 0:
        assert cookie == "wait"
    elif max_age == '0':
        assert cookie is None
    else:
        assert cookie is None