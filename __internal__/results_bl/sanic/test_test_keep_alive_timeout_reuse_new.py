import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.reusable import ReusableClient

app = Sanic("TestApp")

@app.get("/1")
def get_method(request):
    return text('I am get method')

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() == 'Windows', reason='Not testable with current client')
def test_get_method_response(port):
    client = ReusableClient(app, loop=asyncio.new_event_loop(), port=port)
    with client:
        headers = {"Connection": "keep-alive"}
        request, response = client.get("/1", headers=headers)
        assert response.status == 200
        assert response.text == "I am get method"
        assert request.protocol.state["requests_count"] == 1

        request, response = client.get("/1")
        assert response.status == 200
        assert response.text == "I am get method"
        assert request.protocol.state["requests_count"] == 2

def test_get_method_invalid_route(port):
    client = ReusableClient(app, loop=asyncio.new_event_loop(), port=port)
    with client:
        request, response = client.get("/invalid")
        assert response.status == 404

def test_get_method_no_connection_header(port):
    client = ReusableClient(app, loop=asyncio.new_event_loop(), port=port)
    with client:
        request, response = client.get("/1")
        assert response.status == 200
        assert response.text == "I am get method"
        assert request.protocol.state["requests_count"] == 1

def test_get_method_multiple_requests(port):
    client = ReusableClient(app, loop=asyncio.new_event_loop(), port=port)
    with client:
        for _ in range(5):
            request, response = client.get("/1")
            assert response.status == 200
            assert response.text == "I am get method"