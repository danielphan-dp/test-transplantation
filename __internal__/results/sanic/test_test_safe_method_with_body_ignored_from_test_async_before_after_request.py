import json
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.get("/")
    async def handler(request):
        return text("OK")

    return app

def test_request_middleware_run_count(app):
    global request_middleware_run_count
    request_middleware_run_count = 0

    request, response = app.test_client.get("/")

    assert request_middleware_run_count == 1
    assert response.body == b"OK"

def test_request_middleware_with_multiple_requests(app):
    global request_middleware_run_count
    request_middleware_run_count = 0

    app.test_client.get("/")
    app.test_client.get("/")

    assert request_middleware_run_count == 2

def test_request_middleware_with_no_body(app):
    global request_middleware_run_count
    request_middleware_run_count = 0

    payload = {"test": "OK"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.request(
        "/", http_method="get", data=json.dumps(payload), headers=headers
    )

    assert request.body == b""
    assert request.json is None
    assert response.body == b"OK"
    assert request_middleware_run_count == 1

def test_request_middleware_with_invalid_method(app):
    global request_middleware_run_count
    request_middleware_run_count = 0

    request, response = app.test_client.request(
        "/", http_method="post"
    )

    assert request_middleware_run_count == 1
    assert response.status == 405  # Method Not Allowed