import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.get("/")
    async def handler(request):
        return text('I am get method')

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_custom_context(app):
    class CustomContext:
        FOO = "foo"

    class CustomRequest:
        @staticmethod
        def make_context() -> CustomContext:
            return CustomContext()

    app.request_class = CustomRequest

    @app.get("/custom")
    async def custom_handler(request: CustomRequest):
        return text(f'Context FOO is {request.make_context().FOO}')

    request, response = await app.test_client.get("/custom")
    assert response.status == 200
    assert response.text == 'Context FOO is foo'