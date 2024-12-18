import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path, expected_response', [
    ("/get", "I am get method"),
    ("/get/", "I am get method"),
    ("/nonexistent", None),
])
def test_get_method(request_path, expected_response):
    app = Sanic("test_app")

    @app.get("/get")
    def get(request):
        return text("I am get method")

    request, response = app.test_client.get(request_path)

    if expected_response is not None:
        assert response.status == 200
        assert response.text == expected_response
    else:
        assert response.status == 404