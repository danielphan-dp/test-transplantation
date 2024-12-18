import json
import pytest
from sanic import Sanic, Request
from sanic.response import json as json_response
from sanic.response.types import JSONResponse

@pytest.fixture
def json_app():
    app = Sanic("TestApp")

    @app.get("/json")
    async def json_response_handler(request: Request):
        return json_response({"format": request.route.extra.error_format})

    return app

def test_json_response_format(json_app):
    _, response = json_app.test_client.get("/json")
    assert response.status == 200
    assert response.json["format"] == "auto"

def test_json_response_with_invalid_route(json_app):
    _, response = json_app.test_client.get("/invalid-route")
    assert response.status == 404

def test_json_response_with_custom_format(json_app):
    @json_app.get("/json-custom", error_format="json")
    async def custom_json_response(request: Request):
        return json_response({"message": "custom format"})

    _, response = json_app.test_client.get("/json-custom")
    assert response.status == 200
    assert response.json["message"] == "custom format"

def test_json_response_with_no_format(json_app):
    @json_app.get("/json-no-format")
    async def no_format_response(request: Request):
        return json_response({"message": "no format"})

    _, response = json_app.test_client.get("/json-no-format")
    assert response.status == 200
    assert response.json["message"] == "no format"