import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path, expected_status', [
    ("/", 200),
    ("/nonexistent", 404),
    ("/static/test.file/", 200),
    ("/static/test.file", 404),
])
def test_get_method_responses(request_path, expected_status):
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get(request_path)
    assert response.status == expected_status

    if expected_status == 200:
        assert response.text == "I am get method"