import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.reusable import ReusableClient

app = Sanic("TestApp")

@app.get("/test_get")
def get_method(request):
    return text('I am get method')

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() == 'Windows', reason='Not testable with current client')
def test_get_method(port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = ReusableClient(app, loop=loop, port=port)
    
    with client:
        request, response = client.get("/test_get")
        
        assert response.text == "I am get method"
        assert response.status == 200

        # Test with invalid route
        request_invalid, response_invalid = client.get("/invalid_route")
        assert response_invalid.status == 404

        # Test with keep-alive connection
        headers = {"Connection": "keep-alive"}
        request1, response1 = client.get("/test_get", headers=headers)
        request2, response2 = client.get("/test_get", headers=headers)

        assert response1.text == "I am get method"
        assert response2.text == "I am get method"
        assert id(request1.conn_info.ctx) == id(request2.conn_info.ctx)  # Ensure same context
        assert request2.protocol.state["requests_count"] == 2

        # Test response when server is down (simulate)
        app.stop()
        request_down, response_down = client.get("/test_get")
        assert response_down.status == 503  # Assuming 503 for service unavailable