import json
import pytest
from sanic import Sanic, Request
from sanic.response import json as json_response
from sanic.response.types import JSONResponse

@pytest.fixture
def json_app():
    app = Sanic("TestApp")

    @app.get("/json")
    def json_response_handler(request):
        return json_response({"format": request.route.extra.error_format})

    return app

def test_json_response_format(json_app):
    _, response = json_app.test_client.get("/json")
    assert response.status == 200
    assert response.json == {"format": "auto"}

def test_json_response_with_invalid_format(json_app):
    @json_app.get("/json-invalid")
    def invalid_format_handler(request):
        request.route.extra.error_format = "invalid"
        return json_response({"format": request.route.extra.error_format})

    _, response = json_app.test_client.get("/json-invalid")
    assert response.status == 200
    assert response.json == {"format": "invalid"}

def test_json_response_with_no_format(json_app):
    @json_app.get("/json-no-format")
    def no_format_handler(request):
        request.route.extra.error_format = None
        return json_response({"format": request.route.extra.error_format})

    _, response = json_app.test_client.get("/json-no-format")
    assert response.status == 200
    assert response.json == {"format": None}