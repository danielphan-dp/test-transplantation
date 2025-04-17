import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic("Test")

    @app.get("/")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route():
    app = Sanic("Test")

    @app.get("/")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_context():
    class CustomContext:
        FOO = "foo"

    class CustomRequest(Request[Sanic, CustomContext]):
        @staticmethod
        def make_context() -> CustomContext:
            return CustomContext()

    app = Sanic("Test", request_class=CustomRequest)

    @app.get("/")
    async def handler(request: CustomRequest):
        return text(f'I am get method with context: {request.ctx.FOO}')

    request, response = app.test_client.get("/")
    
    assert response.text == "I am get method with context: foo"
    assert response.status == 200