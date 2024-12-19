import pytest
from sanic_testing.reusable import ReusableClient
from sanic.response import json, text

@pytest.mark.asyncio
async def test_get_method(app, port):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    client = ReusableClient(app, port=port)

    with client:
        _, response1 = client.get("/get")
        _, response2 = client.get("/get")

    assert response1.status == response2.status == 200
    assert response1.text == 'I am get method'
    assert response1.text == response2.text
    assert response1.json is None
    assert response2.json is None

    # Testing with a different route to ensure isolation
    @app.get("/another")
    async def another_handler(request):
        return text('I am another method')

    with client:
        _, response3 = client.get("/another")

    assert response3.status == 200
    assert response3.text == 'I am another method'