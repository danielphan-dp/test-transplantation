import json
import pytest
from sanic import Sanic, Request
from sanic.response import json as json_response
from sanic.response.types import JSONResponse

@pytest.fixture
def json_app():
    app = Sanic("TestApp")

    @app.get("/json")
    def json_response_handler(request: Request):
        return json_response({"format": request.route.extra.error_format})

    return app

def test_json_response_format(json_app):
    _, response = json_app.test_client.get("/json")
    assert response.status == 200
    response_data = response.json
    assert response_data == {"format": "json"}

def test_json_response_invalid_format(json_app):
    @json_app.get("/json-invalid")
    def json_invalid_response(request: Request):
        return json_response({"format": "invalid_format"})

    _, response = json_app.test_client.get("/json-invalid")
    assert response.status == 200
    response_data = response.json
    assert response_data == {"format": "invalid_format"}

def test_json_response_empty_format(json_app):
    @json_app.get("/json-empty")
    def json_empty_response(request: Request):
        return json_response({})

    _, response = json_app.test_client.get("/json-empty")
    assert response.status == 200
    response_data = response.json
    assert response_data == {}

def test_json_response_with_query_param(json_app):
    @json_app.get("/json-query")
    def json_query_response(request: Request):
        return json_response({"query": request.args.get("param", "default")})

    _, response = json_app.test_client.get("/json-query?param=test")
    assert response.status == 200
    response_data = response.json
    assert response_data == {"query": "test"}

    _, response = json_app.test_client.get("/json-query")
    assert response.status == 200
    response_data = response.json
    assert response_data == {"query": "default"}