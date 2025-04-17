import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path, expected_response', [
    ("/test", "I am get method"),
    ("/another_test", "I am get method"),
    ("/yet_another_test", "I am get method"),
])
def test_get_method(app: Sanic, request_path, expected_response):
    @app.route(request_path, methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == expected_response

def test_get_method_invalid_route(app: Sanic):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app: Sanic):
    @app.route("/query_test", methods=["GET"])
    def get_method_with_query(request):
        return text('I am get method')

    request, response = app.test_client.get("/query_test?param=value")
    assert response.status == 200
    assert response.text == "I am get method"