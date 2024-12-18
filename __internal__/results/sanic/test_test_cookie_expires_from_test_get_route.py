import pytest
from datetime import datetime, timedelta
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('expires', [timedelta(seconds=60), timedelta(seconds=120)])
def test_get_method(app: Sanic, expires: timedelta):
    @app.get("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"

    expires_time = datetime.utcnow().replace(microsecond=0) + expires
    response.cookies["test"] = "pass"
    response.cookies["test"]["expires"] = expires_time

    cookie_expires = datetime.utcfromtimestamp(
        response.raw_cookies["test"].expires
    ).replace(microsecond=0)

    assert response.cookies["test"] == "pass"
    assert cookie_expires == expires_time

def test_get_method_with_invalid_route(app: Sanic):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app: Sanic):
    @app.get("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers.get("Custom-Header") is None  # Custom headers should not be in response