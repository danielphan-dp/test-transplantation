import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.reusable import ReusableClient

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() != 'Linux', reason='Not testable with current client')
def test_get_method_response(port):
    app = Sanic("test_app")

    @app.get("/test")
    async def get_method(request):
        return text("I am get method")

    client = ReusableClient(app, port=port)

    request, response = client.get("/test")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(port):
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