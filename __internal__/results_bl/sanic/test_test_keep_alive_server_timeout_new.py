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
def test_get_method_valid_response(port):
    client = ReusableClient(app, port=port)
    with client:
        request, response = client.get("/1")
        assert response.status == 200
        assert response.text == "I am get method"

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() == 'Windows', reason='Not testable with current client')
def test_get_method_invalid_route(port):
    client = ReusableClient(app, port=port)
    with client:
        request, response = client.get("/invalid")
        assert response.status == 404

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() == 'Windows', reason='Not testable with current client')
def test_get_method_keep_alive(port):
    loops = 0
    while True:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            client = ReusableClient(app, loop=loop, port=port)
            with client:
                headers = {"Connection": "keep-alive"}
                request, response = client.get("/1", headers=headers, timeout=60)
                assert response.status == 200
                assert response.text == "I am get method"
                assert request.protocol.state["requests_count"] == 1

                loop.run_until_complete(asyncio.sleep(3))
                request, response = client.get("/1", timeout=60)
                assert request.protocol.state["requests_count"] == 1
        except OSError:
            loops += 1
            if loops > 5:
                raise
            continue
        else:
            break

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() == 'Windows', reason='Not testable with current client')
def test_get_method_timeout(port):
    client = ReusableClient(app, port=port)
    with client:
        request, response = client.get("/1", timeout=0.001)
        assert response.status == 504  # Assuming the server has a timeout set for requests.