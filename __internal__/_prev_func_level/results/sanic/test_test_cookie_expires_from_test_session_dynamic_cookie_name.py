import pytest
from datetime import datetime, timedelta
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('expires', [timedelta(seconds=60), timedelta(seconds=120)])
def test_get_method_with_cookie_expires(app: Sanic, expires: timedelta):
    expires_time = datetime.utcnow().replace(microsecond=0) + expires
    cookies = {"test": "wait"}

    @app.get("/")
    def handler(request):
        response = text("I am get method")
        response.cookies["test"] = "pass"
        response.cookies["test"]["expires"] = expires_time
        return response

    request, response = app.test_client.get(
        "/", cookies=cookies, raw_cookies=True
    )

    cookie_expires = datetime.utcfromtimestamp(
        response.raw_cookies["test"].expires
    ).replace(microsecond=0)

    assert response.status == 200
    assert response.text == "I am get method"
    assert response.cookies["test"] == "pass"
    assert cookie_expires == expires_time

def test_get_method_without_cookie(app: Sanic):
    @app.get("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")

    assert response.status == 200
    assert response.text == "I am get method"