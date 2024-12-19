import json
from functools import partial
from unittest.mock import Mock
import pytest
from sanic import Request, Sanic
from sanic.exceptions import SanicException
from sanic.response import json as sanic_json
from sanic.response.types import JSONResponse

@pytest.fixture
def json_app():
    app = Sanic("test_app")
    return app

@app.get('/json')
def json_response(request):
    return sanic_json({'format': request.route.extra.error_format})

def test_json_response_valid_format(json_app):
    @json_app.get("/json")
    async def handler(request: Request):
        request.route.extra = Mock()
        request.route.extra.error_format = "valid_format"
        return json_response(request)

    _, resp = json_app.test_client.get("/json")
    assert resp.body == json.dumps({'format': 'valid_format'}).encode()

def test_json_response_missing_format(json_app):
    @json_app.get("/json")
    async def handler(request: Request):
        request.route.extra = Mock()
        request.route.extra.error_format = None
        return json_response(request)

    _, resp = json_app.test_client.get("/json")
    assert resp.body == json.dumps({'format': None}).encode()

def test_json_response_invalid_format(json_app):
    @json_app.get("/json")
    async def handler(request: Request):
        request.route.extra = Mock()
        request.route.extra.error_format = 12345
        return json_response(request)

    _, resp = json_app.test_client.get("/json")
    assert resp.body == json.dumps({'format': 12345}).encode()