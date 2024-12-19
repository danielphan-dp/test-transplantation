import asyncio
import platform
import pytest
from sanic_testing.reusable import ReusableClient
from sanic import Sanic
from sanic.response import text

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or OS_IS_WINDOWS or platform.system() != 'Linux', reason='Not testable with current client')
def test_get_method_response(port):
    app = Sanic("TestApp")
    
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    loops = 0
    while True:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            client = ReusableClient(app, loop=loop, port=port)
            with client:
                request, response = client.get("/get")
                
                assert response.status == 200
                assert response.text == "I am get method"
                assert request.protocol.state["requests_count"] == 1
        except OSError:
            loops += 1
            if loops > MAX_LOOPS:
                raise
            continue
        else:
            break

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or OS_IS_WINDOWS or platform.system() != 'Linux', reason='Not testable with current client')
def test_get_method_invalid_route(port):
    app = Sanic("TestApp")
    
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    loops = 0
    while True:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            client = ReusableClient(app, loop=loop, port=port)
            with client:
                request, response = client.get("/invalid_route")
                
                assert response.status == 404
                assert response.text == "Not Found"
        except OSError:
            loops += 1
            if loops > MAX_LOOPS:
                raise
            continue
        else:
            break

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or OS_IS_WINDOWS or platform.system() != 'Linux', reason='Not testable with current client')
def test_get_method_with_headers(port):
    app = Sanic("TestApp")
    
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    loops = 0
    while True:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            client = ReusableClient(app, loop=loop, port=port)
            with client:
                headers = {"Custom-Header": "Test"}
                request, response = client.get("/get", headers=headers)
                
                assert response.status == 200
                assert response.text == "I am get method"
                assert request.headers["Custom-Header"] == "Test"
        except OSError:
            loops += 1
            if loops > MAX_LOOPS:
                raise
            continue
        else:
            break