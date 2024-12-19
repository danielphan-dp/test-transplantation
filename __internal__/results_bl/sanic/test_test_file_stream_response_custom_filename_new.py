import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path, expected_body', [
    ("/test", b'I am get method'),
    ("/nonexistent", b'I am get method'),
])
def test_get_method(app: Sanic, request_path, expected_body):
    @app.route("/test", methods=["GET"])
    def test_route(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.body == expected_body

@pytest.mark.parametrize('request_path', [
    ("/invalid_path"),
])
def test_get_method_invalid_path(app: Sanic, request_path):
    @app.route("/test", methods=["GET"])
    def test_route(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 404