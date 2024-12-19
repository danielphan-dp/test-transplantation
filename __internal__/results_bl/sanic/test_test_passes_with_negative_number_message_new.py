import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('number', [0, 1, -1, 2.5, -2.5])
def test_get_method_with_various_numbers(app, number):
    @app.route("/test")
    def get_method(request):
        return text('I am get method')

    u = app.url_for("get_method")
    request, response = app.test_client.get(u)
    assert response.text == 'I am get method'