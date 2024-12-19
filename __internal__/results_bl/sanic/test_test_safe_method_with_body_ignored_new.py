import base64
import logging
import json
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_request_middleware_run_count(app):
    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.get("/")
    async def handler(request):
        return text("OK")

    payload = {"test": "OK"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.request(
        "/", http_method="get", data=json.dumps(payload), headers=headers
    )

    assert request_middleware_run_count == 1
    assert request.body == b""
    assert request.json is None
    assert response.body == b"OK"

def test_request_middleware_multiple_requests(app):
    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.get("/")
    async def handler(request):
        return text("OK")

    for _ in range(5):
        payload = {"test": "OK"}
        headers = {"content-type": "application/json"}
        request, response = app.test_client.request(
            "/", http_method="get", data=json.dumps(payload), headers=headers
        )

    assert request_middleware_run_count == 5
    assert response.body == b"OK"

def test_request_middleware_no_body(app):
    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.get("/")
    async def handler(request):
        return text("OK")

    request, response = app.test_client.request(
        "/", http_method="get"
    )

    assert request_middleware_run_count == 1
    assert request.body == b""
    assert request.json is None
    assert response.body == b"OK"