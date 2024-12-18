import json
import pytest
from sanic import Sanic, Request
from sanic.response import json as json_response
from sanic.exceptions import SanicException

@pytest.fixture
def json_app():
    app = Sanic("TestApp")

    @app.get("/json")
    def json_response_handler(request: Request):
        return json_response({"format": request.route.extra.error_format})

    return app

def test_json_response_format(json_app):
    _, resp = json_app.test_client.get("/json")
    assert resp.status == 200
    assert resp.json == {"format": "json"}

def test_json_response_invalid_format(json_app):
    @json_app.get("/json-invalid")
    def invalid_format_handler(request: Request):
        raise SanicException("Invalid format", status_code=400)

    _, resp = json_app.test_client.get("/json-invalid")
    assert resp.status == 400
    assert resp.json["message"] == "Invalid format"

def test_json_response_with_extra_data(json_app):
    @json_app.get("/json-extra")
    async def extra_data_handler(request: Request):
        return json_response({"format": request.route.extra.error_format, "extra": "data"})

    _, resp = json_app.test_client.get("/json-extra")
    assert resp.status == 200
    assert resp.json == {"format": "json", "extra": "data"}