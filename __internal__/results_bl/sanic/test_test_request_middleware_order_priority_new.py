import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path, expected_response', [
    ("/", "I am get method"),
    ("/nonexistent", "404 Not Found"),
])
def test_get_method(app: Sanic, request_path, expected_response):
    @app.get("/")
    def get_method(request):
        return text('I am get method')

    response = app.test_client.get(request_path)
    
    if request_path == "/":
        assert response.text == expected_response
    else:
        assert response.status == 404