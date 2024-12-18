import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('status', [200, 404, 500])
def test_get_method_response(app: Sanic, status):
    @app.route("/get", methods=["GET"])
    def get_route(request):
        return text('I am get method', status=status)

    request, response = app.test_client.get("/get")
    assert response.status == status
    if status == 200:
        assert response.text == 'I am get method'
    elif status == 404:
        assert response.text == 'Not Found'
    elif status == 500:
        assert response.text == 'Internal Server Error'