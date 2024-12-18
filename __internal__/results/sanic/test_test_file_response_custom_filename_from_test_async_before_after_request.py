import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path, expected_response', [
    ("/get", "I am get method"),
    ("/get/extra", "I am get method"),
    ("/get?query=param", "I am get method"),
])
def test_get_method(app: Sanic, request_path, expected_response):
    @app.route("/get", methods=["GET"])
    def get(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == expected_response

def test_get_method_not_found(app: Sanic):
    @app.route("/get", methods=["GET"])
    def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_headers(app: Sanic):
    @app.route("/get", methods=["GET"])
    def get(request):
        return text('I am get method', headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.headers["X-Custom-Header"] == "value"