import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_method', ['GET', 'POST'])
def test_get_method(app: Sanic, request_method):
    @app.route("/test", methods=["GET", "POST"])
    def test_route(request):
        return text('I am get method')

    request, response = app.test_client.request(request_method, "/test")
    assert response.status == 200
    assert response.body == b'I am get method'

@pytest.mark.parametrize('invalid_method', ['PUT', 'DELETE'])
def test_get_method_invalid(app: Sanic, invalid_method):
    @app.route("/test", methods=["GET"])
    def test_route(request):
        return text('I am get method')

    request, response = app.test_client.request(invalid_method, "/test")
    assert response.status == 405  # Method Not Allowed

def test_get_method_no_route(app: Sanic):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404  # Not Found

def test_get_method_empty_response(app: Sanic):
    @app.route("/empty", methods=["GET"])
    def empty_route(request):
        return text('')

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.body == b''