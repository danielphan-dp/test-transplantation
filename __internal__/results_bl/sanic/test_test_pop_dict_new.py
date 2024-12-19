import json
import pytest
from sanic import Sanic, Request
from sanic.response import json as sanic_json
from sanic.response.types import JSONResponse

@pytest.fixture
def json_app():
    app = Sanic("TestApp")
    return app

@app.get('/json-empty')
async def handler_empty(request: Request):
    return sanic_json({})

def test_json_response_empty(json_app):
    _, resp = json_app.test_client.get("/json-empty")
    assert resp.body == json.dumps({}).encode()

@app.get('/json-invalid')
async def handler_invalid(request: Request):
    return sanic_json({"format": None})

def test_json_response_invalid(json_app):
    _, resp = json_app.test_client.get("/json-invalid")
    assert resp.body == json.dumps({"format": None}).encode()

@app.get('/json-missing-format')
async def handler_missing_format(request: Request):
    return sanic_json({"other_key": "value"})

def test_json_response_missing_format(json_app):
    _, resp = json_app.test_client.get("/json-missing-format")
    assert resp.body == json.dumps({"other_key": "value"}).encode()

@app.get('/json-error-format')
async def handler_error_format(request: Request):
    request.route.extra.error_format = "error"
    return sanic_json({"format": request.route.extra.error_format})

def test_json_response_error_format(json_app):
    _, resp = json_app.test_client.get("/json-error-format")
    assert resp.body == json.dumps({"format": "error"}).encode()