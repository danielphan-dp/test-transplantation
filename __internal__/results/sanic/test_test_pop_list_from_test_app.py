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
    assert response.json == {"format": "auto"}

def test_json_response_invalid_format(json_app):
    @json_app.get("/json-invalid")
    def invalid_format_handler(request: Request):
        request.route.extra.error_format = "invalid_format"
        return json_response({"format": request.route.extra.error_format})

    _, response = json_app.test_client.get("/json-invalid")
    assert response.status == 200
    assert response.json == {"format": "invalid_format"}

def test_json_response_empty_format(json_app):
    @json_app.get("/json-empty")
    def empty_format_handler(request: Request):
        request.route.extra.error_format = ""
        return json_response({"format": request.route.extra.error_format})

    _, response = json_app.test_client.get("/json-empty")
    assert response.status == 200
    assert response.json == {"format": ""}

def test_json_response_with_query_param(json_app):
    @json_app.get("/json-query")
    def query_param_handler(request: Request):
        return json_response({"query": request.args.get("param", "default")})

    _, response = json_app.test_client.get("/json-query?param=test")
    assert response.status == 200
    assert response.json == {"query": "test"}

    _, response = json_app.test_client.get("/json-query")
    assert response.status == 200
    assert response.json == {"query": "default"}