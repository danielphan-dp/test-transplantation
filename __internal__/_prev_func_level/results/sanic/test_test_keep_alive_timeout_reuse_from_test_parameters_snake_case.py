import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() == 'Windows', reason='Not testable with current client')
def test_get_method_response(port):
    app = Sanic("test_app")

    @app.get("/test-get")
    async def get_method(request):
        return text("I am get method")

    client = app.test_client

    request, response = client.get("/test-get")
    assert response.status == 200
    assert response.text == "I am get method"

    request, response = client.get("/test-get")
    assert response.status == 200
    assert response.text == "I am get method"