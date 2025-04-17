import pytest
from sanic_testing.reusable import ReusableClient
from sanic.response import text

@pytest.mark.asyncio
async def test_post_method_response(app, port):
    @app.post("/")
    async def handler(request):
        return text('I am post method')

    client = ReusableClient(app, port=port)

    with client:
        request, response = client.post("/")
    
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_different_requests(app, port):
    @app.post("/")
    async def handler(request):
        return text('I am post method')

    client = ReusableClient(app, port=port)

    with client:
        request1, response1 = client.post("/")
        request2, response2 = client.post("/")

    assert response1.status == response2.status == 200
    assert response1.text == response2.text == 'I am post method'
    assert request1.id != request2.id

@pytest.mark.asyncio
async def test_post_method_with_invalid_route(app, port):
    @app.post("/valid")
    async def handler(request):
        return text('I am post method')

    client = ReusableClient(app, port=port)

    with client:
        request, response = client.post("/invalid")

    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.asyncio
async def test_post_method_with_empty_body(app, port):
    @app.post("/")
    async def handler(request):
        return text('I am post method')

    client = ReusableClient(app, port=port)

    with client:
        request, response = client.post("/", data={})

    assert response.status == 200
    assert response.text == 'I am post method'