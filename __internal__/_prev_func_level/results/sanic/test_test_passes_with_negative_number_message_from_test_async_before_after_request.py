import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.mark.parametrize('number', [3, -3, 13.123, -13.123])
def test_get_method_with_various_numbers(app, number):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.as_view(), "/get")

    u = app.url_for("dummyview.get")
    assert u == "/get", u
    request, response = app.test_client.get(u)
    assert response.text == "I am get method"