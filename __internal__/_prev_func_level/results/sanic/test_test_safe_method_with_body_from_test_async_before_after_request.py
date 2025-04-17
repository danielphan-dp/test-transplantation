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

    app.test_client.get("/")
    assert request_middleware_run_count == 1

def test_multiple_requests_increments_count(app):
    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.get("/")
    async def handler(request):
        return text("OK")

    app.test_client.get("/")
    app.test_client.get("/")
    assert request_middleware_run_count == 2

def test_request_middleware_with_payload(app):
    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.get("/", ignore_body=False)
    async def handler(request):
        return text("OK")

    payload = {"test": "OK"}
    headers = {"content-type": "application/json"}
    data = json.dumps(payload)
    request, response = app.test_client.request(
        "/", http_method="get", data=data, headers=headers
    )

    assert request.body == data.encode("utf-8")
    assert request.json.get("test") == "OK"
    assert response.body == b"OK"
    assert request_middleware_run_count == 1

def test_request_middleware_no_body(app):
    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.get("/")
    async def handler(request):
        return text("OK")

    request, response = app.test_client.get("/")
    assert request_middleware_run_count == 1
    assert response.body == b"OK"