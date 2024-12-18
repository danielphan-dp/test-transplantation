import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestManager

@pytest.fixture
def app():
    app = Sanic("TestApp")

    request_middleware_run_count = 0

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    @app.get("/")
    async def handler(request):
        return text("OK")

    return app

def test_request_middleware_run_count(app):
    test_client = SanicTestManager(app)

    request, response = test_client.get("/")
    
    assert request.body == b""
    assert request.json is None
    assert response.body == b"OK"
    assert app.request_middleware_run_count == 1

def test_request_middleware_multiple_requests(app):
    test_client = SanicTestManager(app)

    for _ in range(5):
        test_client.get("/")

    assert app.request_middleware_run_count == 5

def test_request_middleware_no_body(app):
    test_client = SanicTestManager(app)

    payload = {"test": "OK"}
    headers = {"content-type": "application/json"}

    request, response = test_client.request(
        "/", http_method="get", data=json.dumps(payload), headers=headers
    )

    assert request.body == b""
    assert request.json is None
    assert response.body == b"OK"
    assert app.request_middleware_run_count == 1

def test_request_middleware_with_different_methods(app):
    test_client = SanicTestManager(app)

    request, response = test_client.post("/", data={"key": "value"})
    assert response.body == b"OK"
    assert app.request_middleware_run_count == 1

    request, response = test_client.put("/", data={"key": "value"})
    assert response.body == b"OK"
    assert app.request_middleware_run_count == 2

    request, response = test_client.delete("/")
    assert response.body == b"OK"
    assert app.request_middleware_run_count == 3