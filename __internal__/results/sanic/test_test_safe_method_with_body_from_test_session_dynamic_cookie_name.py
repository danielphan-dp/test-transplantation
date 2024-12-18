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

def test_multiple_requests_increments_count(app):
    global request_middleware_run_count
    request_middleware_run_count = 0

    app.test_client.get("/")
    app.test_client.get("/")

    assert request_middleware_run_count == 2

def test_request_middleware_with_different_methods(app):
    global request_middleware_run_count
    request_middleware_run_count = 0

    app.test_client.post("/", data={"test": "data"})
    app.test_client.put("/", data={"test": "data"})

    assert request_middleware_run_count == 2

def test_request_middleware_with_no_requests(app):
    global request_middleware_run_count
    request_middleware_run_count = 0

    assert request_middleware_run_count == 0