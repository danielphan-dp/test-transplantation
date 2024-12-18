import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.reusable import ReusableClient

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() == 'Windows', reason='Not testable with current client')
async def test_get_method_response(port):
    app = Sanic("test_app")

    @app.get("/test-get")
    async def get_method(request):
        return text("I am get method")

    client = ReusableClient(app, port=port)

    async with client:
        request, response = await client.get("/test-get")
        assert response.status == 200
        assert response.text == "I am get method"

        # Test with additional headers
        headers = {"Custom-Header": "Test"}
        request, response = await client.get("/test-get", headers=headers)
        assert response.status == 200
        assert response.text == "I am get method"
        assert request.headers["Custom-Header"] == "Test"

        # Test with invalid route
        request, response = await client.get("/invalid-route")
        assert response.status == 404

        # Test with keep-alive
        headers = {"Connection": "keep-alive"}
        request, response = await client.get("/test-get", headers=headers)
        assert response.status == 200
        assert response.text == "I am get method"