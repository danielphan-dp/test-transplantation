import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize("request_path", ["/", "/test"])
def test_get_method(app: Sanic, request_path):
    @app.route(request_path, methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize("invalid_path", ["/invalid", "/notfound"])
def test_get_method_invalid_path(app: Sanic, invalid_path):
    @app.route("/valid", methods=["GET"])
    def valid_get(request):
        return text('I am get method')

    request, response = app.test_client.get(invalid_path)
    assert response.status == 404
    assert "Requested URL" in response.text

def test_get_method_with_query_params(app: Sanic):
    @app.route("/get_with_params", methods=["GET"])
    def get_with_params(request):
        return text(f"I am get method with params: {request.args}")

    request, response = app.test_client.get("/get_with_params?param1=value1&param2=value2")
    assert response.status == 200
    assert response.text == "I am get method with params: {'param1': ['value1'], 'param2': ['value2']}"