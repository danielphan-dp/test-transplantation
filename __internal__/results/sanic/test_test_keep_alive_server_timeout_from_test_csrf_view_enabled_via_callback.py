import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import ReusableClient

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() == 'Windows', reason='Not testable with current client')
def test_get_method_response(port):
    app = Sanic("test_app")

    @app.get("/test")
    async def get_method(request):
        return text("I am get method")

    client = ReusableClient(app, port=port)

    request, response = client.get("/test")

    assert response.status == 200
    assert response.text == "I am get method"
    assert request.protocol.state["requests_count"] == 1

def test_get_method_invalid_route(port):
    app = Sanic("test_app")

    @app.get("/test")
    async def get_method(request):
        return text("I am get method")

    client = ReusableClient(app, port=port)

    request, response = client.get("/invalid_route")

    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_keep_alive(port):
    app = Sanic("test_app")

    @app.get("/keep_alive")
    async def get_method(request):
        return text("I am get method")

    client = ReusableClient(app, port=port)

    headers = {"Connection": "keep-alive"}
    request, response = client.get("/keep_alive", headers=headers)

    assert response.status == 200
    assert response.text == "I am get method"
    assert request.protocol.state["requests_count"] == 1

    request, response = client.get("/keep_alive", headers=headers)

    assert request.protocol.state["requests_count"] == 2

def test_get_method_with_custom_header(port):
    app = Sanic("test_app")

    @app.get("/custom_header")
    async def get_method(request):
        return text("I am get method")

    client = ReusableClient(app, port=port)

    headers = {"X-Custom-Header": "TestValue"}
    request, response = client.get("/custom_header", headers=headers)

    assert response.status == 200
    assert response.text == "I am get method"
    assert request.headers["X-Custom-Header"] == "TestValue"