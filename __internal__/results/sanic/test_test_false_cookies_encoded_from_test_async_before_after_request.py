import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('expected', [200, 404])
def test_get_method_response(app, expected):
    @app.route("/get")
    def get_method(request):
        return text("I am get method", status=expected)

    request, response = app.test_client.get("/get")

    assert response.status == expected
    assert response.text == "I am get method" if expected == 200 else "Not Found"