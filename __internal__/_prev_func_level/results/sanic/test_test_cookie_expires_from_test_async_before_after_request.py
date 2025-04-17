import pytest
from datetime import datetime, timedelta
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('expires', [timedelta(seconds=60), timedelta(seconds=120)])
def test_get_method(app: Sanic, expires: timedelta):
    expires_time = datetime.utcnow().replace(microsecond=0) + expires
    cookies = {"test": "wait"}

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get(
        "/get", cookies=cookies, raw_cookies=True
    )

    assert response.status == 200
    assert response.text == "I am get method"