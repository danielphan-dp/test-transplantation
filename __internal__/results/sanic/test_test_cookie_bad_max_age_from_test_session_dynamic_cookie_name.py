import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('max_age', [0, -1, 'invalid'])
def test_get_method_with_invalid_max_age(app, max_age):
    @app.get("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/", cookies={"test": "wait"}, raw_cookies=True)
    assert response.status == 200
    assert response.text == "I am get method"