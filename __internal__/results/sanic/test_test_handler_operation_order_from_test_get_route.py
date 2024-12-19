import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request):
        return text('I am get method')

    return app

@pytest.mark.asyncio
async def test_get_method_response(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_empty_request(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    request, response = await app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming the handler does not change based on params

@pytest.mark.asyncio
async def test_get_method_with_headers(app):
    request, response = await app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming the handler does not change based on headers

@pytest.mark.asyncio
async def test_get_method_order_of_operations(app):
    operations = []

    @app.on_request
    async def on_request(_):
        operations.append(1)

    @app.on_response
    async def on_response(*_):
        operations.append(5)

    @app.signal(Event.HTTP_HANDLER_BEFORE)
    async def handler_before(**_):
        operations.append(2)

    @app.signal(Event.HTTP_HANDLER_AFTER)
    async def handler_after(**_):
        operations.append(4)

    await app.test_client.get("/")
    assert operations == [1, 2, 3, 4, 5]  # Ensure the order of operations is correct