import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path, expected_response', [
    ("/get", "I am get method"),
    ("/get/extra", "I am get method"),
    ("/get?query=param", "I am get method"),
])
def test_get_method_responses(app: Sanic, request_path, expected_response):
    @app.route("/get", methods=["GET"])
    def get(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == expected_response

@pytest.mark.parametrize('invalid_path', [
    "/invalid",
    "/get/another/invalid/path",
])
def test_get_method_invalid_paths(app: Sanic, invalid_path):
    @app.route("/get", methods=["GET"])
    def get(request):
        return text('I am get method')

    request, response = app.test_client.get(invalid_path)
    assert response.status == 404
    assert "Requested URL" in response.text

def test_get_method_with_headers(app: Sanic):
    @app.route("/get", methods=["GET"])
    def get(request):
        return text('I am get method', headers={'X-Custom-Header': 'value'})

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'value'