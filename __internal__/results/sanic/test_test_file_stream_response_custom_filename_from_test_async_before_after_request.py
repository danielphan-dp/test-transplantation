import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path, expected_response', [
    ("/get", "I am get method"),
    ("/get/extra", "I am get method"),  # Testing with an extra path segment
    ("/get?query=param", "I am get method"),  # Testing with query parameters
])
def test_get_method(app: Sanic, request_path, expected_response):
    @app.route("/get", methods=["GET"])
    def get(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == expected_response

def test_get_method_invalid_route(app: Sanic):
    @app.route("/get", methods=["GET"])
    def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_headers(app: Sanic):
    @app.route("/get", methods=["GET"])
    def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers.get("Custom-Header") is None  # Ensure custom header is not in response