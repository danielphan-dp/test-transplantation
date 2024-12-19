import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path, expected_status, expected_body', [
    ("/get", 200, "I am get method"),
    ("/nonexistent", 404, "Not Found"),
])
def test_get_method(app: Sanic, request_path, expected_status, expected_body):
    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    @app.get("/nonexistent")
    def nonexistent_method(request):
        raise SanicException("Not Found", status_code=404)

    _, response = app.test_client.get(request_path)
    assert response.status == expected_status
    assert response.text == expected_body if expected_status == 200 else response.text == "Not Found"