import json
import pytest
from sanic import Sanic, Request
from sanic.response import json as sanic_json
from sanic.response.types import JSONResponse

@pytest.fixture
def json_app():
    app = Sanic("TestApp")
    return app

@app.get('/json')
def json_response(request):
    return sanic_json({'format': request.route.extra.error_format})

def test_json_response_empty(json_app: Sanic):
    @json_app.get("/json-empty")
    async def handler_empty(request: Request):
        return json_response(request)

    _, resp = json_app.test_client.get("/json-empty")
    assert resp.json == {'format': None}

def test_json_response_invalid_route(json_app: Sanic):
    @json_app.get("/json-invalid")
    async def handler_invalid(request: Request):
        request.route.extra.error_format = None
        return json_response(request)

    _, resp = json_app.test_client.get("/json-invalid")
    assert resp.json == {'format': None}

def test_json_response_with_format(json_app: Sanic):
    @json_app.get("/json-format")
    async def handler_format(request: Request):
        request.route.extra.error_format = "custom_format"
        return json_response(request)

    _, resp = json_app.test_client.get("/json-format")
    assert resp.json == {'format': 'custom_format'}

def test_json_response_no_format(json_app: Sanic):
    @json_app.get("/json-no-format")
    async def handler_no_format(request: Request):
        request.route.extra.error_format = ""
        return json_response(request)

    _, resp = json_app.test_client.get("/json-no-format")
    assert resp.json == {'format': ''}