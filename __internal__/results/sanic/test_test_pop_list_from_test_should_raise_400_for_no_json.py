import pytest
from sanic import Sanic, Request
from sanic.response import json
from sanic.response.types import JSONResponse

@pytest.fixture
def json_app():
    app = Sanic("TestApp")

    @app.get("/json")
    def json_response(request):
        return json({'format': request.route.extra.error_format})

    return app

def test_json_response_format(json_app):
    _, response = json_app.test_client.get("/json")
    assert response.status == 200
    assert response.json['format'] == 'auto'

def test_json_response_with_invalid_route(json_app):
    @json_app.get("/invalid-json")
    async def invalid_json_response(request: Request):
        return json({'error': 'Invalid route'}, status=404)

    _, response = json_app.test_client.get("/invalid-json")
    assert response.status == 404
    assert response.json['error'] == 'Invalid route'

def test_json_response_with_custom_error_format(json_app):
    @json_app.get("/json-custom")
    async def custom_json_response(request: Request):
        request.route.extra.error_format = 'json'
        return json({'format': request.route.extra.error_format})

    _, response = json_app.test_client.get("/json-custom")
    assert response.status == 200
    assert response.json['format'] == 'json'

def test_json_response_with_no_format(json_app):
    @json_app.get("/json-no-format")
    async def no_format_response(request: Request):
        request.route.extra.error_format = None
        return json({'format': request.route.extra.error_format})

    _, response = json_app.test_client.get("/json-no-format")
    assert response.status == 200
    assert response.json['format'] is None

def test_json_response_with_empty_request(json_app):
    @json_app.get("/json-empty")
    async def empty_request_response(request: Request):
        return json({})

    _, response = json_app.test_client.get("/json-empty")
    assert response.status == 200
    assert response.json == {}