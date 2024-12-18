import pytest
from datetime import datetime, timedelta
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('max_age', ['0', 30, '30', -1, 'invalid'])
def test_get_method_with_cookie_max_age(app, max_age):
    cookies = {"test": "wait"}

    @app.get("/")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(
        "/", cookies=cookies, raw_cookies=True
    )
    assert response.status == 200
    assert response.text == 'I am get method'

    cookie = response.cookies.get("test")
    if (
        str(max_age).isdigit()
        and int(max_age) == float(max_age)
        and int(max_age) != 0
    ):
        cookie_expires = datetime.utcfromtimestamp(
            response.raw_cookies["test"].expires
        ).replace(microsecond=0)

        expires = datetime.utcnow().replace(microsecond=0) + timedelta(
            seconds=int(max_age)
        )

        assert cookie == "wait"
        assert (
            cookie_expires == expires
            or cookie_expires == expires + timedelta(seconds=-1)
        )
    else:
        assert cookie is None

@pytest.mark.parametrize('invalid_method', ['POST', 'PUT', 'DELETE'])
def test_get_method_invalid_http_methods(app, invalid_method):
    @app.get("/")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/", method=invalid_method)
    assert response.status == 405
    assert "Method GET not allowed for URL /" in response.text