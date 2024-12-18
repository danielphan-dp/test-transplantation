import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('max_age', [30.0, 30.1, 'test'])
def test_get_method_with_cookies(app, max_age):
    cookies = {"test": "wait"}

    @app.get("/")
    def handler(request):
        response = text("I am get method")
        response.cookies["test"] = "pass"
        response.cookies["test"]["max-age"] = max_age
        return response

    request, response = app.test_client.get(
        "/", cookies=cookies, raw_cookies=True
    )
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.cookies["test"].value == "pass"
    assert response.cookies["test"]["max-age"] == max_age