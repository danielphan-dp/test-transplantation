import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('number', [3, -3, 13.123, -13.123])
def test_get_method(app, number):
    @app.route("/get")
    class GetView:
        def get(self, request):
            return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'