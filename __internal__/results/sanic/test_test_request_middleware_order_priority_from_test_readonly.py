import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize("expected_response", [
    "I am get method",
])
def test_get_method_response(app: Sanic, expected_response):
    @app.get("/")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == expected_response

@pytest.mark.parametrize("invalid_path", [
    "/invalid",
])
def test_get_method_invalid_path(app: Sanic, invalid_path):
    @app.get("/")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(invalid_path)
    
    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize("method", [
    "POST",
    "PUT",
    "DELETE",
])
def test_get_method_invalid_method(app: Sanic, method):
    @app.get("/")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.dispatch(method, "/")
    
    assert response.status == 405
    assert "Method" in response.text
    assert "not allowed" in response.text