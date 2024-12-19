import pytest
from sanic_testing.reusable import ReusableClient
from sanic.response import text

@pytest.mark.asyncio
async def test_post_method(app, port):
    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    client = ReusableClient(app, port=port)

    with client:
        _, response = client.post("/post")

    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_invalid_data(app, port):
    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    client = ReusableClient(app, port=port)

    with client:
        _, response = client.post("/post", data="invalid data")

    assert response.status == 200
    assert response.text == 'I am post method'