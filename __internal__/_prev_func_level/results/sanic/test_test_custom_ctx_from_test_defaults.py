import pytest
from sanic import Sanic, response
from sanic.response import text

app = Sanic("Test")

@app.get("/get")
async def get_handler(request):
    return text('I am get method')

def test_get_method():
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_invalid_route():
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_context():
    class CustomContext:
        FOO = "foo"

    class CustomRequest:
        @staticmethod
        def make_context() -> CustomContext:
            return CustomContext()

    app = Sanic("Test", request_class=CustomRequest)

    @app.get("/custom")
    async def custom_handler(request: CustomRequest):
        return response.json(
            [
                isinstance(request, CustomRequest),
                isinstance(request.ctx, CustomContext),
                request.ctx.FOO,
            ]
        )

    _, resp = app.test_client.get("/custom")
    assert resp.json == [True, True, "foo"]