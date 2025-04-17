import json
import pytest
from sanic import Sanic, Request
from sanic.response import json as json_response
from sanic.exceptions import SanicException

@pytest.fixture
def json_app():
    app = Sanic("TestApp")

    @app.get('/json')
    async def json_response_handler(request: Request):
        return json_response({"format": request.route.extra.error_format})

    return app

def test_json_response_format(json_app):
    json_app.get('/json', error_format='json')
    _, resp = json_app.test_client.get('/json')
    assert resp.status == 200
    assert resp.json == {"format": "json"}

def test_json_response_invalid_format(json_app):
    json_app.get('/json', error_format='invalid_format')
    _, resp = json_app.test_client.get('/json')
    assert resp.status == 500
    assert resp.json['message'] == "Unknown format: invalid_format"

def test_json_response_no_format(json_app):
    json_app.get('/json')
    _, resp = json_app.test_client.get('/json')
    assert resp.status == 200
    assert resp.json == {"format": "auto"}

def test_json_response_with_query_param(json_app):
    @json_app.get('/json-query')
    async def json_query_handler(request: Request):
        return json_response({"format": request.args.get('format', 'auto')})

    _, resp = json_app.test_client.get('/json-query?format=json')
    assert resp.status == 200
    assert resp.json == {"format": "json"}