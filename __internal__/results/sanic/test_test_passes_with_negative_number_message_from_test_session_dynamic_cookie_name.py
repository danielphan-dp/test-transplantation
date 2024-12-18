import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('number', [3, -3, 13.123, -13.123])
def test_get_method(app, number):
    @app.route("/get")
    def get(request):
        return text('I am get method')

    u = app.url_for("get")
    assert u == "/get", u
    request, response = app.test_client.get(u)
    assert response.text == "I am get method"